import sys
import supabase_utils

class GateImporter:
    def __init__(self, rollback_on_failure=True):
        self.rollback_on_failure = rollback_on_failure
        # Stack to keep track of inserted records in case we need to roll back
        # Format: (table_name, primary_key_dict)
        self.inserted_records = []
        
        # Caching layers to minimize database calls
        self.subject_cache = {}       # code -> id
        self.topic_cache = {}         # (subject_id, topic_name) -> id
        self.paper_cache = {}         # (exam, year, set_number) -> id
        self.concept_cache = {}       # concept_name -> id
        self.tag_cache = {}           # tag_name -> id
        self.prerequisite_cache = {}  # prereq_name -> id

    def track_insert(self, table, record):
        """Track inserted ID for rollback purposes."""
        if 'id' in record:
            self.inserted_records.append((table, {"id": record["id"]}))

    def rollback(self):
        """Roll back all inserts made in the current session in reverse order."""
        if not self.inserted_records:
            print("No records to roll back.")
            return
        
        print("\n[WARNING] An error occurred. Starting rollback of inserted records...")
        # Roll back in reverse order (LIFO)
        for table, pk_dict in reversed(self.inserted_records):
            try:
                print(f"Rolling back {table} (ID: {pk_dict.get('id')})...")
                supabase_utils.delete(table, pk_dict)
            except Exception as rollback_err:
                print(f"Failed to roll back {table} {pk_dict}: {rollback_err}")
        print("Rollback completed.\n")

    def get_or_create_subject(self, subject_data):
        code = subject_data.get("subject_code")
        name = subject_data.get("subject_name")
        
        if code in self.subject_cache:
            return self.subject_cache[code]
        
        # Look up or create subject
        lookup = {"code": code}
        create_fields = {
            "name": name,
            "color": subject_data.get("color"),
            "icon": subject_data.get("icon"),
            "display_order": subject_data.get("display_order", 0)
        }
        
        subject, created = supabase_utils.get_or_create("gate_subjects", lookup, create_fields)
        if created:
            self.track_insert("gate_subjects", subject)
            print(f"[NEW] Created Subject: '{name}' ({code})")
        else:
            print(f"[EXISTING] Found existing Subject: '{name}' ({code})")
            
        self.subject_cache[code] = subject["id"]
        return subject["id"]

    def import_topics(self, subject_id, topics):
        print(f"Processing {len(topics)} topics...")
        for index, t in enumerate(topics):
            name = t.get("topic_name")
            summary = t.get("summary")
            display_order = t.get("display_order", index)
            
            cache_key = (subject_id, name)
            if cache_key in self.topic_cache:
                continue
                
            lookup = {"subject_id": subject_id, "name": name}
            create_fields = {
                "summary": summary,
                "display_order": display_order
            }
            
            topic, created = supabase_utils.get_or_create("gate_topics", lookup, create_fields)
            if created:
                self.track_insert("gate_topics", topic)
            self.topic_cache[cache_key] = topic["id"]

    def get_or_create_paper(self, src):
        exam = src.get("exam", "GATE CSE")
        year = src.get("year")
        set_number = src.get("set")  # can be null
        
        cache_key = (exam, year, set_number)
        if cache_key in self.paper_cache:
            return self.paper_cache[cache_key]
            
        lookup = {
            "exam": exam,
            "year": year,
            "set_number": set_number
        }
        
        paper, created = supabase_utils.get_or_create("gate_papers", lookup)
        if created:
            self.track_insert("gate_papers", paper)
            print(f"[NEW] Created Paper: {exam} {year} Set {set_number}")
            
        self.paper_cache[cache_key] = paper["id"]
        return paper["id"]

    def get_or_create_concept(self, name):
        if name in self.concept_cache:
            return self.concept_cache[name]
            
        lookup = {"name": name}
        concept, created = supabase_utils.get_or_create("gate_concepts", lookup)
        if created:
            self.track_insert("gate_concepts", concept)
            
        self.concept_cache[name] = concept["id"]
        return concept["id"]

    def get_or_create_tag(self, name):
        if name in self.tag_cache:
            return self.tag_cache[name]
            
        lookup = {"name": name}
        tag, created = supabase_utils.get_or_create("gate_tags", lookup)
        if created:
            self.track_insert("gate_tags", tag)
            
        self.tag_cache[name] = tag["id"]
        return tag["id"]

    def get_or_create_prerequisite(self, name):
        if name in self.prerequisite_cache:
            return self.prerequisite_cache[name]
            
        lookup = {"name": name}
        prereq, created = supabase_utils.get_or_create("gate_prerequisites", lookup)
        if created:
            self.track_insert("gate_prerequisites", prereq)
            
        self.prerequisite_cache[name] = prereq["id"]
        return prereq["id"]

    def import_question(self, subject_id, q_data):
        question_text = q_data.get("question_text")
        
        # Check if question already exists in this subject (Idempotency)
        existing = supabase_utils.select("gate_questions", {
            "subject_id": subject_id,
            "question_text": question_text
        })
        
        if existing:
            # Question exists, skip creation
            return existing[0]["id"], False
            
        # Create new question
        q_fields = {
            "subject_id": subject_id,
            "question_text": question_text,
            "question_type": q_data.get("question_type"),
            "difficulty": q_data.get("difficulty"),
            "marks": q_data.get("marks"),
            "explanation": q_data.get("explanation"),
            "correct_answer_text": q_data.get("correct_answer_text"),
            "learning_objective": q_data.get("learning_objective"),
            "revision_priority": q_data.get("revision_priority"),
            "blooms_taxonomy": q_data.get("blooms_taxonomy"),
            "is_numerical": q_data.get("is_numerical", False),
            "formula_based": q_data.get("formula_based", False),
            "estimated_solve_time_seconds": q_data.get("estimated_solve_time_seconds")
        }
        
        res = supabase_utils.insert("gate_questions", q_fields)
        if not res:
            raise Exception("Failed to insert question.")
            
        q_record = res[0]
        q_id = q_record["id"]
        self.track_insert("gate_questions", q_record)
        
        # 1. Mappings to Topics
        for t_name in q_data.get("topics", []):
            topic_id = self.topic_cache.get((subject_id, t_name))
            if not topic_id:
                # Fallback check if it was not preloaded
                topic, created = supabase_utils.get_or_create("gate_topics", {"subject_id": subject_id, "name": t_name})
                if created:
                    self.track_insert("gate_topics", topic)
                topic_id = topic["id"]
                self.topic_cache[(subject_id, t_name)] = topic_id
                
            q_topic_res = supabase_utils.insert("gate_question_topics", {
                "question_id": q_id,
                "topic_id": topic_id
            })
            if q_topic_res:
                self.track_insert("gate_question_topics", q_topic_res[0])
                
        # 2. Options
        for opt in q_data.get("options", []):
            opt_fields = {
                "question_id": q_id,
                "option_label": opt.get("label"),
                "option_text": opt.get("text"),
                "is_correct": opt.get("is_correct", False)
            }
            opt_res = supabase_utils.insert("gate_options", opt_fields)
            if opt_res:
                self.track_insert("gate_options", opt_res[0])
                
        # 3. Occurrences (Papers)
        for src in q_data.get("pyq_sources", []):
            paper_id = self.get_or_create_paper(src)
            occ_fields = {
                "question_id": q_id,
                "paper_id": paper_id,
                "question_number": src.get("question_number"),
                "marks": src.get("marks", q_data.get("marks"))
            }
            occ_res = supabase_utils.insert("gate_question_occurrences", occ_fields)
            if occ_res:
                self.track_insert("gate_question_occurrences", occ_res[0])
                
        # 4. Concepts
        for c_name in q_data.get("concepts", []):
            concept_id = self.get_or_create_concept(c_name)
            q_concept_res = supabase_utils.insert("gate_question_concepts", {
                "question_id": q_id,
                "concept_id": concept_id
            })
            if q_concept_res:
                self.track_insert("gate_question_concepts", q_concept_res[0])
                
        # 5. Tags
        for tag_name in q_data.get("tags", []):
            tag_id = self.get_or_create_tag(tag_name)
            q_tag_res = supabase_utils.insert("gate_question_tags", {
                "question_id": q_id,
                "tag_id": tag_id
            })
            if q_tag_res:
                self.track_insert("gate_question_tags", q_tag_res[0])

        # 6. Prerequisites
        for prereq_name in q_data.get("prerequisites", []):
            prereq_id = self.get_or_create_prerequisite(prereq_name)
            q_prereq_res = supabase_utils.insert("gate_question_prerequisites", {
                "question_id": q_id,
                "prerequisite_id": prereq_id
            })
            if q_prereq_res:
                self.track_insert("gate_question_prerequisites", q_prereq_res[0])

        # 7. Common Mistakes
        mistakes = q_data.get("common_mistakes", [])
        if isinstance(mistakes, str):
            mistakes = [mistakes]
        for mistake in mistakes:
            mistake_res = supabase_utils.insert("gate_common_mistakes", {
                "question_id": q_id,
                "mistake": mistake
            })
            if mistake_res:
                self.track_insert("gate_common_mistakes", mistake_res[0])

        # 8. Related Concepts
        related = q_data.get("related_concepts", [])
        if isinstance(related, str):
            related = [related]
        for concept in related:
            related_res = supabase_utils.insert("gate_related_concepts", {
                "question_id": q_id,
                "concept": concept
            })
            if related_res:
                self.track_insert("gate_related_concepts", related_res[0])
                
        return q_id, True

    def run_import(self, import_data):
        """Main method to execute the import flow."""
        try:
            # 1. Subject creation/retrieval
            subject_data = import_data.get("subject")
            if not subject_data:
                raise ValueError("Subject details are missing in input data.")
            subject_id = self.get_or_create_subject(subject_data)
            
            # 2. Topic creation/retrieval
            topics_data = import_data.get("topics", [])
            self.import_topics(subject_id, topics_data)
            
            # 3. Questions and mapping insertion
            questions_data = import_data.get("questions", [])
            total_questions = len(questions_data)
            print(f"Processing {total_questions} questions...")
            
            created_count = 0
            skipped_count = 0
            
            for index, q_data in enumerate(questions_data, start=1):
                # Simple progress indicator
                pct = int((index / total_questions) * 100)
                sys.stdout.write(f"\rImporting questions: {index}/{total_questions} [{pct}%]")
                sys.stdout.flush()
                
                _, created = self.import_question(subject_id, q_data)
                if created:
                    created_count += 1
                else:
                    skipped_count += 1
                    
            print(f"\n\n[SUCCESS] Import completed successfully!")
            print(f"[CREATED] New questions created: {created_count}")
            print(f"[SKIPPED] Questions skipped (already exist): {skipped_count}")
            
        except Exception as err:
            print(f"\n[ERROR] Error during import: {err}")
            if self.rollback_on_failure:
                self.rollback()
            raise err
