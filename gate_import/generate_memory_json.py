import json

subject = {
    "subject_name": "Operating System",
    "subject_code": "OS"
}

topics = [
    {"topic_name": "Linking and Loading", "summary": "Static/dynamic linking, relocation, and loading of programs into memory."},
    {"topic_name": "Paging", "summary": "Basic paging concepts, page tables, page table entries, and address translation."},
    {"topic_name": "Multi-level Page Tables", "summary": "Hierarchical (multi-level) page table organization, sizing, and overhead calculations."},
    {"topic_name": "Segmentation", "summary": "Segmented memory management and overhead of segment tables."},
    {"topic_name": "TLB", "summary": "Translation Look-aside Buffer organization, hit ratio, tag sizing, and reach."},
    {"topic_name": "Effective Access Time", "summary": "Computing average/effective memory access time considering TLB, cache, and page faults."},
    {"topic_name": "Demand Paging", "summary": "Demand paging systems, page fault handling, and dirty page write-back."},
    {"topic_name": "Page Replacement Algorithms", "summary": "FIFO, LRU, Optimal, MRU, LIFO, and Random page replacement policies and their comparison."},
    {"topic_name": "Belady's Anomaly", "summary": "Anomalous increase in page faults with increased frames for certain replacement policies."},
    {"topic_name": "Memory Allocation", "summary": "Contiguous memory allocation strategies: best-fit, first-fit, next-fit, worst-fit."},
    {"topic_name": "Fragmentation", "summary": "Internal and external fragmentation issues in memory management."},
    {"topic_name": "Cache Memory", "summary": "Cache organization, associativity, replacement policy, and virtually/physically indexed caches."},
    {"topic_name": "Virtual Memory", "summary": "Virtual memory concepts, benefits, and relationship to physical memory."},
    {"topic_name": "Inverted and Hashed Page Tables", "summary": "Alternative page table organizations such as inverted and hashed page tables."},
    {"topic_name": "Memory Management Unit", "summary": "Responsibilities of the MMU including address translation and trap generation."},
    {"topic_name": "Disk Scheduling", "summary": "Disk head scheduling algorithms and their effect on I/O performance."}
]

questions = []

def add(q):
    questions.append(q)

add({
    "question_text": "The process of assigning load addresses to the various parts of the program and adjusting the code and data in the program to reflect the assigned addresses is called",
    "question_type": "MCQ",
    "marks": 1,
    "difficulty": "easy",
    "topics": ["Linking and Loading"],
    "concepts": ["Relocation", "Load address assignment"],
    "tags": ["loader", "relocation", "linking"],
    "is_numerical": False,
    "formula_based": False,
    "estimated_solve_time_seconds": 30,
    "options": [
        {"label": "A", "text": "assembly", "is_correct": False},
        {"label": "B", "text": "parsing", "is_correct": False},
        {"label": "C", "text": "relocation", "is_correct": True},
        {"label": "D", "text": "symbol resolution", "is_correct": False}
    ],
    "correct_answer_text": None,
    "explanation": "Relocation can change the assigned address of data and code in the program.",
    "pyq_sources": [{"year": 2001, "set": 1, "question_number": "4.11", "marks": 1}]
})

add({
    "question_text": "Consider a virtual memory system with FIFO page replacement policy. For an arbitrary page access pattern, increasing the number of page frames in main memory will",
    "question_type": "MCQ",
    "marks": 1,
    "difficulty": "medium",
    "topics": ["Page Replacement Algorithms", "Belady's Anomaly"],
    "concepts": ["FIFO page replacement", "Belady's anomaly"],
    "tags": ["fifo", "page faults", "belady's anomaly", "virtual memory"],
    "is_numerical": False,
    "formula_based": False,
    "estimated_solve_time_seconds": 60,
    "options": [
        {"label": "A", "text": "always decrease the number of page faults", "is_correct": False},
        {"label": "B", "text": "always increase the number of page faults", "is_correct": False},
        {"label": "C", "text": "sometimes increase the number of page faults", "is_correct": True},
        {"label": "D", "text": "never affect the number of page faults", "is_correct": False}
    ],
    "correct_answer_text": None,
    "explanation": "Belady's Anomaly: increasing the number of frames can sometimes increase the number of page faults, and this is observed with the FIFO replacement policy.",
    "pyq_sources": [{"year": 2001, "set": 1, "question_number": "4.12", "marks": 1}]
})

add({
    "question_text": "Which of the following is not a form of memory?",
    "question_type": "MCQ",
    "marks": 1,
    "difficulty": "easy",
    "topics": ["Cache Memory"],
    "concepts": ["Memory hierarchy", "Instruction format"],
    "tags": ["cache", "register", "instruction opcode"],
    "is_numerical": False,
    "formula_based": False,
    "estimated_solve_time_seconds": 30,
    "options": [
        {"label": "A", "text": "Instruction cache", "is_correct": False},
        {"label": "B", "text": "Instruction register", "is_correct": False},
        {"label": "C", "text": "Instruction opcode", "is_correct": True},
        {"label": "D", "text": "Translation look a side buffer", "is_correct": False}
    ],
    "correct_answer_text": None,
    "explanation": "Instruction cache, instruction register, and TLB are memories, but instruction opcode is the part of an instruction that specifies the operation to perform.",
    "pyq_sources": [{"year": 2002, "set": 1, "question_number": "4.13", "marks": 1}]
})

add({
    "question_text": "The optimal page replacement algorithm will, select the page that",
    "question_type": "MCQ",
    "marks": 1,
    "difficulty": "easy",
    "topics": ["Page Replacement Algorithms"],
    "concepts": ["Optimal page replacement"],
    "tags": ["optimal replacement", "page faults"],
    "is_numerical": False,
    "formula_based": False,
    "estimated_solve_time_seconds": 30,
    "options": [
        {"label": "A", "text": "Has not been used for the longest time in the past", "is_correct": False},
        {"label": "B", "text": "Will not be used for the longest time in the future", "is_correct": True},
        {"label": "C", "text": "Has been used least number of times", "is_correct": False},
        {"label": "D", "text": "Has been used most number of times", "is_correct": False}
    ],
    "correct_answer_text": None,
    "explanation": "The optimal page replacement algorithm selects a page that will not be used for the longest time in the future.",
    "pyq_sources": [{"year": 2002, "set": 1, "question_number": "4.14", "marks": 1}]
})

add({
    "question_text": "Dynamic linking can cause security concerns because",
    "question_type": "MCQ",
    "marks": 2,
    "difficulty": "easy",
    "topics": ["Linking and Loading"],
    "concepts": ["Dynamic linking", "Security"],
    "tags": ["dynamic linking", "libraries", "security"],
    "is_numerical": False,
    "formula_based": False,
    "estimated_solve_time_seconds": 30,
    "options": [
        {"label": "A", "text": "Security is dynamic", "is_correct": False},
        {"label": "B", "text": "The path for searching dynamic libraries is not known till runtime", "is_correct": True},
        {"label": "C", "text": "Linking is insecure", "is_correct": False},
        {"label": "D", "text": "Cryptographic procedures are not available for dynamic linking", "is_correct": False}
    ],
    "correct_answer_text": None,
    "explanation": "In dynamic linking, the path for searching dynamic libraries is not known till runtime, i.e., it keeps changing, which can create a security concern.",
    "pyq_sources": [{"year": 2002, "set": 1, "question_number": "4.15", "marks": 2}]
})

add({
    "question_text": "In a system with 32 bit virtual addresses and 1 KB page size, use of one-level page tables for virtual to physical address translation is not practical because of",
    "question_type": "MCQ",
    "marks": 1,
    "difficulty": "medium",
    "topics": ["Paging", "Multi-level Page Tables"],
    "concepts": ["One-level page table overhead"],
    "tags": ["page table", "page size", "overhead"],
    "is_numerical": True,
    "formula_based": True,
    "estimated_solve_time_seconds": 60,
    "options": [
        {"label": "A", "text": "the large amount of internal fragmentation", "is_correct": False},
        {"label": "B", "text": "the large amount of external fragmentation", "is_correct": False},
        {"label": "C", "text": "the large memory overhead in maintaining page tables", "is_correct": True},
        {"label": "D", "text": "the large computation overhead in the translation process", "is_correct": False}
    ],
    "correct_answer_text": None,
    "explanation": "Given page size = 1 KB = 2^10 bytes and virtual address is 32 bits long, so required number of pages = 2^32 / 2^10 = 2^22, which is very large, causing a large memory overhead in maintaining page tables.",
    "pyq_sources": [{"year": 2003, "set": 1, "question_number": "4.16", "marks": 1}]
})

add({
    "question_text": "Common Data for Q. 4.17 & 4.18: A processor uses 2-level page tables for virtual to physical address translation. Page tables for both levels are stored in the main memory. Virtual and physical addresses are both 32 bits wide. The memory is byte addressable. For virtual to physical address translation, the 10 most significant bits of the virtual address are used as index into the first level page table while the next 10 bits are used as index into the second level page table. The 12 least significant bits of the virtual address are used as offset within the page. Assume that the page table entries in both levels of page tables are 4 bytes wide. Further, the processor has a translation look-aside buffer (TLB), with a hit rate of 96%. The TLB caches recently used virtual page numbers and the corresponding physical page numbers. The processor also has a physically addressed cache with a hit ratio of 90%. Main memory access time is 10 ns, cache access time is 1 ns, and TLB access time is also 1 ns. Assuming that no page faults occur, the average time taken to access a virtual address is approximately (to the nearest 0.5 ns)",
    "question_type": "MCQ",
    "marks": 2,
    "difficulty": "hard",
    "topics": ["TLB", "Effective Access Time", "Multi-level Page Tables"],
    "concepts": ["TLB hit ratio", "cache hit ratio", "two-level page table"],
    "tags": ["tlb", "cache", "average access time", "two-level paging"],
    "is_numerical": True,
    "formula_based": True,
    "estimated_solve_time_seconds": 180,
    "options": [
        {"label": "A", "text": "1.5 ns", "is_correct": False},
        {"label": "B", "text": "2 ns", "is_correct": False},
        {"label": "C", "text": "3 ns", "is_correct": False},
        {"label": "D", "text": "4 ns", "is_correct": True}
    ],
    "correct_answer_text": None,
    "explanation": "Average time taken to access a virtual address = [(96/100)(1 + 0.9*1 + 0.1*(1+10))] + [(0.04)(21 + 0.9*1 + 0.1*(1+10))] = [(.96)(1+0.9+0.1*11)] + [(0.04)(21+0.9+0.1*11)] = 3.87 ns \u2248 4 ns.",
    "pyq_sources": [{"year": 2003, "set": 2, "question_number": "4.17", "marks": 2}]
})

add({
    "question_text": "Common Data for Q. 4.17 & 4.18 (same setup as Q4.17). Suppose a process has only the following pages in its virtual address space: two contiguous code pages starting at virtual address 0x00000000, two contiguous data pages starting at virtual address 0x00400000, and a stack page starting at virtual address 0xFFFFF000. The amount of memory required for storing the page tables of this process is",
    "question_type": "MCQ",
    "marks": 2,
    "difficulty": "hard",
    "topics": ["Multi-level Page Tables"],
    "concepts": ["Two-level page table sizing"],
    "tags": ["page table size", "two-level paging", "virtual address space"],
    "is_numerical": True,
    "formula_based": True,
    "estimated_solve_time_seconds": 180,
    "options": [
        {"label": "A", "text": "8 KB", "is_correct": False},
        {"label": "B", "text": "12 KB", "is_correct": False},
        {"label": "C", "text": "16 KB", "is_correct": True},
        {"label": "D", "text": "20 KB", "is_correct": False}
    ],
    "correct_answer_text": None,
    "explanation": "The first, second, and third virtual addresses all map to entries in different blocks of the first-level page table, requiring all 4 second-level page tables (one per first-level entry range used) to be brought into main memory. Total memory required = 4 x 2^10 x 4 B = 16 KB.",
    "pyq_sources": [{"year": 2003, "set": 2, "question_number": "4.18", "marks": 2}]
})

add({
    "question_text": "Consider an operating system capable of loading and executing a single sequential user process at a time. The disk head scheduling algorithm used is First Come First Served (FCFS). If FCFS is replaced by Shortest Seek Time First (SSTF), claimed by the vendor to given 50% better benchmark results, what is the expected improvement in the I/O performance of user programs?",
    "question_type": "MCQ",
    "marks": 1,
    "difficulty": "medium",
    "topics": ["Disk Scheduling"],
    "concepts": ["FCFS vs SSTF disk scheduling", "I/O performance"],
    "tags": ["disk scheduling", "sstf", "fcfs", "i/o performance"],
    "is_numerical": False,
    "formula_based": False,
    "estimated_solve_time_seconds": 60,
    "options": [
        {"label": "A", "text": "50%", "is_correct": False},
        {"label": "B", "text": "40%", "is_correct": False},
        {"label": "C", "text": "25%", "is_correct": False},
        {"label": "D", "text": "0%", "is_correct": True}
    ],
    "correct_answer_text": None,
    "explanation": "I/O performance of a user program is determined by many input and output devices, not only by the disk. Replacing FCFS with SSTF improves only disk driver performance, not the entire I/O performance. So the I/O performance improvement of the user program is 0%.",
    "pyq_sources": [{"year": 2004, "set": 1, "question_number": "4.19", "marks": 1}]
})

add({
    "question_text": "The minimum number of page frames that must be allocated to a running process in a virtual memory environment is determined by",
    "question_type": "MCQ",
    "marks": 1,
    "difficulty": "medium",
    "topics": ["Virtual Memory", "Paging"],
    "concepts": ["Minimum page frames", "instruction set architecture"],
    "tags": ["virtual memory", "page frames", "instruction set architecture"],
    "is_numerical": False,
    "formula_based": False,
    "estimated_solve_time_seconds": 30,
    "options": [
        {"label": "A", "text": "the instruction set architecture", "is_correct": True},
        {"label": "B", "text": "page size", "is_correct": False},
        {"label": "C", "text": "physical memory size", "is_correct": False},
        {"label": "D", "text": "number of processes in memory", "is_correct": False}
    ],
    "correct_answer_text": None,
    "explanation": "Minimum number of page frames allocated to a running process is determined by the instruction set architecture (e.g., number of memory operands an instruction can have).",
    "pyq_sources": [{"year": 2004, "set": 1, "question_number": "4.20", "marks": 1}]
})

add({
    "question_text": "Consider a system with a two-level paging scheme in which a regular memory access takes 150 nanoseconds, and servicing a page fault takes 8 milliseconds. An average instruction takes 100 nanoseconds of CPU time, and two memory accesses. The TLB hit ratio is 90%, and the page fault rate is one in every 10,000 instructions. What is the effective average instruction execution time?",
    "question_type": "MCQ",
    "marks": 2,
    "difficulty": "hard",
    "topics": ["Effective Access Time", "TLB", "Demand Paging"],
    "concepts": ["Effective instruction execution time", "TLB hit ratio", "page fault rate"],
    "tags": ["effective access time", "tlb", "page fault rate", "two-level paging"],
    "is_numerical": True,
    "formula_based": True,
    "estimated_solve_time_seconds": 180,
    "options": [
        {"label": "A", "text": "645 nanoseconds", "is_correct": False},
        {"label": "B", "text": "1050 nanoseconds", "is_correct": False},
        {"label": "C", "text": "1215 nanoseconds", "is_correct": False},
        {"label": "D", "text": "1260 nanoseconds", "is_correct": True}
    ],
    "correct_answer_text": None,
    "explanation": "Effective average instruction execution time = CPU time (100 ns) + Average time lost due to page fault per instruction (8 ms / 10000) + Number of memory references x EMAT = 100 + 800 + 2 x [0.9(0+150) + 0.1(0 + 3x150)] = 1260 ns.",
    "pyq_sources": [{"year": 2004, "set": 2, "question_number": "4.21", "marks": 2}]
})

add({
    "question_text": "Consider a fully associative cache with 8 cache blocks (numbered 0-7) and the following sequence of memory block requests: 4, 3, 25, 8, 19, 6, 25, 8, 16, 35, 45, 22, 8, 3, 16, 25, 7. If LRU replacement policy is used, which cache block will have memory block 7?",
    "question_type": "MCQ",
    "marks": 2,
    "difficulty": "medium",
    "topics": ["Cache Memory"],
    "concepts": ["Fully associative cache", "LRU replacement"],
    "tags": ["cache", "lru", "fully associative"],
    "is_numerical": True,
    "formula_based": False,
    "estimated_solve_time_seconds": 120,
    "options": [
        {"label": "A", "text": "4", "is_correct": False},
        {"label": "B", "text": "5", "is_correct": True},
        {"label": "C", "text": "6", "is_correct": False},
        {"label": "D", "text": "7", "is_correct": False}
    ],
    "correct_answer_text": None,
    "explanation": "Tracing the LRU replacement sequence for the 8 fully-associative cache blocks over the given request sequence, memory block 7 ends up placed in cache block 5 (B5).",
    "pyq_sources": [{"year": 2004, "set": 2, "question_number": "4.22", "marks": 2}]
})

add({
    "question_text": "In a virtual memory system, size of virtual address is 32-bit, size of physical address is 30-bit, page size is 4 Kbyte and size of each page table entry is 32-bit. The main memory is byte addressable. Which one of the following is the maximum number of bits that can be used for storing protection and other information in each page table entry?",
    "question_type": "MCQ",
    "marks": 2,
    "difficulty": "medium",
    "topics": ["Paging"],
    "concepts": ["Page table entry composition"],
    "tags": ["page table entry", "protection bits", "frame number"],
    "is_numerical": True,
    "formula_based": True,
    "estimated_solve_time_seconds": 120,
    "options": [
        {"label": "A", "text": "2", "is_correct": False},
        {"label": "B", "text": "10", "is_correct": False},
        {"label": "C", "text": "12", "is_correct": False},
        {"label": "D", "text": "14", "is_correct": True}
    ],
    "correct_answer_text": None,
    "explanation": "Number of frames = physical memory / page size = 2^30 / 2^12 = 2^18, requiring 18 bits for the frame number. Page table entry = frame number bits + other bits, so 32 = 18 + x, giving x = 14 bits available for protection and other information.",
    "pyq_sources": [{"year": 2004, "set": 2, "question_number": "4.23", "marks": 2}]
})

add({
    "question_text": "For each of the four processes P1, P2, P3 and P4, the total size in kilobytes (KB) and the number of segments are given below: P1: 195 KB, 4 segments; P2: 254 KB, 5 segments; P3: 45 KB, 3 segments; P4: 364 KB, 8 segments. The page size is 1 KB. The size of an entry in the page table is 4 bytes. The size of an entry in the segment table is 8 bytes. The maximum size of a segment is 256 KB. The paging method for memory management uses two-level paging and its storage overhead is P. The storage overhead for the segmentation method is S. The storage overhead for the segmentation and paging method is T. What is the relation among the overheads for the different methods of memory management in the concurrent execution of the above four processes?",
    "question_type": "MCQ",
    "marks": 2,
    "difficulty": "hard",
    "topics": ["Segmentation", "Multi-level Page Tables"],
    "concepts": ["Two-level paging overhead", "segmentation overhead", "segmented paging overhead"],
    "tags": ["segmentation", "paging overhead", "segment table", "page table"],
    "is_numerical": True,
    "formula_based": True,
    "estimated_solve_time_seconds": 180,
    "options": [
        {"label": "A", "text": "P < S < T", "is_correct": False},
        {"label": "B", "text": "S < P < T", "is_correct": True},
        {"label": "C", "text": "S < T < P", "is_correct": False},
        {"label": "D", "text": "T < S < P", "is_correct": False}
    ],
    "correct_answer_text": None,
    "explanation": "Overhead using two-level paging (P) = 4104 bytes. Overhead using segmentation (S) = 256 bytes. Overhead using segmentation and paging (T) = 5376 bytes. So S < P < T.",
    "pyq_sources": [{"year": 2006, "set": 2, "question_number": "4.24", "marks": 2}]
})

add({
    "question_text": "A CPU generates 32-bit virtual addresses. The page size is 4 KB. The processor has a translation look-aside buffer (TLB) which can hold a total of 128 page table entries and is 4-way set associative. The minimum size of the TLB tag is",
    "question_type": "MCQ",
    "marks": 2,
    "difficulty": "medium",
    "topics": ["TLB"],
    "concepts": ["Set-associative TLB tag sizing"],
    "tags": ["tlb", "set associative", "tag bits"],
    "is_numerical": True,
    "formula_based": True,
    "estimated_solve_time_seconds": 120,
    "options": [
        {"label": "A", "text": "11 bits", "is_correct": False},
        {"label": "B", "text": "13 bits", "is_correct": False},
        {"label": "C", "text": "15 bits", "is_correct": True},
        {"label": "D", "text": "20 bits", "is_correct": False}
    ],
    "correct_answer_text": None,
    "explanation": "Number of bits for virtual address = 32; number of bits for page offset = log2(4KB) = 12, so bits for page number = 32-12 = 20. Number of sets = 128/4 = 32, requiring log2(32) = 5 bits for set index. Minimum tag size = 20 - 5 = 15 bits.",
    "pyq_sources": [{"year": 2006, "set": 2, "question_number": "4.25", "marks": 2}]
})

add({
    "question_text": "A computer system supports 32-bit virtual addresses as well as 32-bit physical addresses. Since the virtual address space is of the same size as the physical address space, the operating system designers decide to get rid of the virtual memory entirely. Which one of the following is true?",
    "question_type": "MCQ",
    "marks": 2,
    "difficulty": "medium",
    "topics": ["Virtual Memory"],
    "concepts": ["Purpose of virtual memory", "multiprogramming"],
    "tags": ["virtual memory", "multiprogramming", "multi-user support"],
    "is_numerical": False,
    "formula_based": False,
    "estimated_solve_time_seconds": 90,
    "options": [
        {"label": "A", "text": "Efficient implementation of multi-user support is no longer possible", "is_correct": True},
        {"label": "B", "text": "The processor cache organization can be made more efficient now", "is_correct": False},
        {"label": "C", "text": "Hardware support for memory management is no longer needed", "is_correct": False},
        {"label": "D", "text": "CPU scheduling can be made more efficient now", "is_correct": False}
    ],
    "correct_answer_text": None,
    "explanation": "The main purpose of virtual memory is to allow processes to use less physical memory at a time, increasing the degree of multiprogramming by bringing more processes into memory. Removing virtual memory means efficient implementation of multiprogramming and multi-user support is no longer possible.",
    "pyq_sources": [{"year": 2006, "set": 2, "question_number": "4.26", "marks": 2}]
})

add({
    "question_text": "Let a memory have four free blocks of sizes 4k, 8k, 20k, 2k. These blocks are allocated following the best-fit strategy. The allocation requests are stored in a queue as shown below: Request No. J1: size 2k, usage time 4; J2: size 14k, usage time 10; J3: size 3k, usage time 2; J4: size 6k, usage time 8; J5: size 6k, usage time 4; J6: size 10k, usage time 1; J7: size 7k, usage time 8; J8: size 20k, usage time 6. The time at which the request for J7 will be completed will be",
    "question_type": "MCQ",
    "marks": 1,
    "difficulty": "hard",
    "topics": ["Memory Allocation"],
    "concepts": ["Best-fit allocation", "job scheduling with holes"],
    "tags": ["best-fit", "memory allocation", "free blocks"],
    "is_numerical": True,
    "formula_based": False,
    "estimated_solve_time_seconds": 180,
    "options": [
        {"label": "A", "text": "16", "is_correct": False},
        {"label": "B", "text": "19", "is_correct": True},
        {"label": "C", "text": "20", "is_correct": False},
        {"label": "D", "text": "37", "is_correct": False}
    ],
    "correct_answer_text": None,
    "explanation": "Tracing the best-fit allocation of the four free blocks against the queued requests over time, the request for J7 completes at time 19.",
    "pyq_sources": [{"year": 2007, "set": 1, "question_number": "4.27", "marks": 1}]
})

add({
    "question_text": "The address sequence generated by tracing a particular program executing in a pure demand paging system with 100 bytes per page is 0100, 0200, 0430, 0499, 0510, 0530, 0560, 0120, 0220, 0240, 0260, 0320, 0410. Suppose that the memory can store only one page and if x is the address which causes a page fault then the bytes from addresses x to x + 99 are loaded on to the memory. How many page faults will occur?",
    "question_type": "MCQ",
    "marks": 1,
    "difficulty": "medium",
    "topics": ["Demand Paging"],
    "concepts": ["Page fault tracing", "single-frame demand paging"],
    "tags": ["demand paging", "page fault", "address sequence"],
    "is_numerical": True,
    "formula_based": False,
    "estimated_solve_time_seconds": 120,
    "options": [
        {"label": "A", "text": "0", "is_correct": False},
        {"label": "B", "text": "4", "is_correct": False},
        {"label": "C", "text": "7", "is_correct": True},
        {"label": "D", "text": "8", "is_correct": False}
    ],
    "correct_answer_text": None,
    "explanation": "Tracing each reference address against the currently loaded 100-byte window: faults occur at 0100, 0200, 0430, 0530, 0120, 0220, 0320, giving a total of 7 page faults.",
    "pyq_sources": [{"year": 2007, "set": 1, "question_number": "4.28", "marks": 1}]
})

add({
    "question_text": "A demand paging system takes 100 time units to service a page fault and 300 time units to replace a dirty page. Memory access time is 1 time unit. The probability of a page fault is p. In case of a page fault, the probability of page being dirty is also p. It is observed that the average access time is 3 time units. Then the value of p is",
    "question_type": "MCQ",
    "marks": 2,
    "difficulty": "hard",
    "topics": ["Demand Paging", "Effective Access Time"],
    "concepts": ["Average access time with dirty page probability"],
    "tags": ["demand paging", "dirty page", "average access time", "quadratic equation"],
    "is_numerical": True,
    "formula_based": True,
    "estimated_solve_time_seconds": 180,
    "options": [
        {"label": "A", "text": "0.194", "is_correct": True},
        {"label": "B", "text": "0.233", "is_correct": False},
        {"label": "C", "text": "0.514", "is_correct": False},
        {"label": "D", "text": "0.981", "is_correct": False}
    ],
    "correct_answer_text": None,
    "explanation": "Average Access Time = (1-p)(T_mem) + p[p(S.T. dirty) + (1-p)(S.T. not dirty)]. Substituting values: 3 = (1-p)(1) + p(p*300) + (1-p)(100), which simplifies to 200p^2 + 99p - 2 = 0, giving p = 0.194.",
    "pyq_sources": [{"year": 2007, "set": 2, "question_number": "4.29", "marks": 2}]
})

add({
    "question_text": "Common Data for Q. 4.30 & 4.31: A process has been allocated 3 page frames. Assume that none of the pages of the process are available in the memory initially. The process makes the following sequence of page references (reference string): 1, 2, 1, 3, 7, 4, 5, 6, 3, 1. If optimal page replacement policy is used, how many page faults occur for the above reference string?",
    "question_type": "MCQ",
    "marks": 2,
    "difficulty": "medium",
    "topics": ["Page Replacement Algorithms"],
    "concepts": ["Optimal page replacement"],
    "tags": ["optimal replacement", "page faults", "reference string"],
    "is_numerical": True,
    "formula_based": False,
    "estimated_solve_time_seconds": 120,
    "options": [
        {"label": "A", "text": "7", "is_correct": True},
        {"label": "B", "text": "8", "is_correct": False},
        {"label": "C", "text": "9", "is_correct": False},
        {"label": "D", "text": "10", "is_correct": False}
    ],
    "correct_answer_text": None,
    "explanation": "Tracing the reference string 1,2,1,3,7,4,5,6,3,1 with 3 frames using optimal replacement gives a total of 7 page faults.",
    "pyq_sources": [{"year": 2007, "set": 2, "question_number": "4.30", "marks": 2}]
})

add({
    "question_text": "Least Recently Used (LRU) page replacement policy is a practical approximation to optimal page replacement. For the reference string 1, 2, 1, 3, 7, 4, 5, 6, 3, 1 with 3 page frames (none available initially), how many more page faults occur with LRU than with the optimal page replacement policy?",
    "question_type": "MCQ",
    "marks": 2,
    "difficulty": "medium",
    "topics": ["Page Replacement Algorithms"],
    "concepts": ["LRU vs optimal comparison"],
    "tags": ["lru", "optimal replacement", "page faults", "reference string"],
    "is_numerical": True,
    "formula_based": False,
    "estimated_solve_time_seconds": 120,
    "options": [
        {"label": "A", "text": "0", "is_correct": False},
        {"label": "B", "text": "1", "is_correct": False},
        {"label": "C", "text": "2", "is_correct": True},
        {"label": "D", "text": "3", "is_correct": False}
    ],
    "correct_answer_text": None,
    "explanation": "Tracing the same reference string with LRU gives 9 page faults, while optimal gives 7. Difference = 9 - 7 = 2 more page faults with LRU.",
    "pyq_sources": [{"year": 2007, "set": 2, "question_number": "4.31", "marks": 2}]
})

add({
    "question_text": "A paging scheme uses a Translation Look-aside Buffer (TLB). A TLB-access takes 10 ns and a main memory access takes 50 ns. What is the effective access time (in ns) if the TLB hit ratio is 90% and there is no page-fault?",
    "question_type": "MCQ",
    "marks": 1,
    "difficulty": "medium",
    "topics": ["TLB", "Effective Access Time"],
    "concepts": ["TLB hit ratio", "effective access time"],
    "tags": ["tlb", "hit ratio", "effective access time"],
    "is_numerical": True,
    "formula_based": True,
    "estimated_solve_time_seconds": 90,
    "options": [
        {"label": "A", "text": "54", "is_correct": False},
        {"label": "B", "text": "60", "is_correct": False},
        {"label": "C", "text": "65", "is_correct": True},
        {"label": "D", "text": "75", "is_correct": False}
    ],
    "correct_answer_text": None,
    "explanation": "Effective access time = hit ratio * (TLB access time + memory access time) + miss ratio * (TLB access time + page table access time + memory access time) = 0.9*(10+50) + 0.1*(10+50+50) = 54 + 11 = 65 ns.",
    "pyq_sources": [{"year": 2008, "set": 1, "question_number": "4.32", "marks": 1}]
})

add({
    "question_text": "A processor uses 36 bit physical addresses and 32 bit virtual addresses, with a page frame size of 4 Kbytes. Each page table entry is of size 4 bytes. A three level page table is used for virtual-to-physical address translation, where the virtual address is used as follows: bits 30-31 are used to index into the first level page table, bits 21-29 are used to index into the second level page table, bits 12-20 are used to index into the third level page table, bits 0-11 are used as offset within the page. The number of bits required for addressing the next level page table (or page frame) in the page table entry of the first, second and third level page tables are respectively.",
    "question_type": "MCQ",
    "marks": 2,
    "difficulty": "hard",
    "topics": ["Multi-level Page Tables"],
    "concepts": ["Three-level page table addressing"],
    "tags": ["three-level paging", "page table entry", "physical address"],
    "is_numerical": True,
    "formula_based": True,
    "estimated_solve_time_seconds": 180,
    "options": [
        {"label": "A", "text": "20, 20 and 20", "is_correct": False},
        {"label": "B", "text": "24, 24, and 24", "is_correct": True},
        {"label": "C", "text": "24, 24 and 20", "is_correct": False},
        {"label": "D", "text": "25, 25 and 24", "is_correct": False}
    ],
    "correct_answer_text": None,
    "explanation": "Since page tables are stored in main memory divided into frames, addressing a page table entry requires the same number of bits as addressing the frames. The number of bits required for addressing frames at each level is 24 (physical address 36 bits, frame offset 12 bits, giving 24 bits for frame number).",
    "pyq_sources": [{"year": 2008, "set": 2, "question_number": "4.33", "marks": 2}]
})

add({
    "question_text": "Assume that a main memory with only 4 pages, each of 16 bytes, is initially empty. The CPU generates the following sequence of virtual addresses and uses the Least Recently Used (LRU) page replacement policy: 0, 4, 8, 20, 24, 36, 44, 12, 68, 72, 80, 84, 28, 32, 88, 92. How many page faults does this sequence cause? What are the page numbers of the pages present in the main memory at the end of the sequence?",
    "question_type": "MCQ",
    "marks": 2,
    "difficulty": "hard",
    "topics": ["Page Replacement Algorithms"],
    "concepts": ["LRU page replacement", "page number extraction from address"],
    "tags": ["lru", "page faults", "virtual address"],
    "is_numerical": True,
    "formula_based": True,
    "estimated_solve_time_seconds": 180,
    "options": [
        {"label": "A", "text": "6 and 1, 2, 3, 4", "is_correct": False},
        {"label": "B", "text": "7 and 1, 2, 4, 5", "is_correct": True},
        {"label": "C", "text": "8 and 1, 2, 4, 5", "is_correct": False},
        {"label": "D", "text": "9 and 1, 2, 3, 5", "is_correct": False}
    ],
    "correct_answer_text": None,
    "explanation": "Since page size = frame size = 16 bytes, the least significant 4 bits of each address represent the offset and the remaining bits represent the page number. Tracing the resulting page number sequence 0,0,0,1,1,4,2,0,4,4,5,5,1,2,5,5 with LRU and 4 frames results in 7 page faults, with pages 1, 2, 4, 5 present in memory at the end.",
    "pyq_sources": [{"year": 2008, "set": 2, "question_number": "4.34", "marks": 2}]
})

add({
    "question_text": "Match the following flag bits used in the context of virtual memory management on the List-I (Name of the bit) with the different purposes on the List-II (Purpose) of the table below: List-I: I. Dirty, II. R/W, III. Reference, IV. Valid. List-II: a. Page initialization, b. Write-back policy, c. Page protection, d. Page replacement policy. Codes: (a) I-d, II-a, III-b, IV-c (b) I-b, II-c, III-d, IV-a (c) I-c, II-d, III-a, IV-b (d) I-b, II-c, III-d, IV-a",
    "question_type": "MCQ",
    "marks": 2,
    "difficulty": "medium",
    "topics": ["Paging"],
    "concepts": ["Page table flag bits: dirty, R/W, reference, valid"],
    "tags": ["dirty bit", "valid bit", "reference bit", "page table flags"],
    "is_numerical": False,
    "formula_based": False,
    "estimated_solve_time_seconds": 90,
    "options": [
        {"label": "A", "text": "I-d, II-a, III-b, IV-c", "is_correct": False},
        {"label": "B", "text": "I-b, II-c, III-d, IV-a", "is_correct": False},
        {"label": "C", "text": "I-c, II-d, III-a, IV-b", "is_correct": False},
        {"label": "D", "text": "I-b, II-c, III-d, IV-a", "is_correct": True}
    ],
    "correct_answer_text": None,
    "explanation": "Dirty bit is used for write-back policy. R/W bit is used for page protection. Reference bit is used in page replacement policy (e.g., second chance policy). Valid bit is used for page initialization. Note: the source document lists identical text for options (b) and (d) due to an apparent OCR/printing artifact in the original book; the answer key marks (d) as correct.",
    "pyq_sources": [{"year": 2008, "set": 2, "question_number": "4.35", "marks": 2}]
})

add({
    "question_text": "In which one of the following page replacement policies, Bleady's anomaly may occur?",
    "question_type": "MCQ",
    "marks": 1,
    "difficulty": "easy",
    "topics": ["Belady's Anomaly", "Page Replacement Algorithms"],
    "concepts": ["Belady's anomaly"],
    "tags": ["belady's anomaly", "fifo", "page replacement"],
    "is_numerical": False,
    "formula_based": False,
    "estimated_solve_time_seconds": 30,
    "options": [
        {"label": "A", "text": "FIFO", "is_correct": True},
        {"label": "B", "text": "Optimal", "is_correct": False},
        {"label": "C", "text": "LRU", "is_correct": False},
        {"label": "D", "text": "MRU", "is_correct": False}
    ],
    "correct_answer_text": None,
    "explanation": "In Belady's Anomaly, if the number of frames is increased, the number of page faults increases. This behavior is found only with FIFO.",
    "pyq_sources": [{"year": 2009, "set": 1, "question_number": "4.36", "marks": 1}]
})

add({
    "question_text": "The essential content(s) in each entry of a page table is/are",
    "question_type": "MCQ",
    "marks": 1,
    "difficulty": "easy",
    "topics": ["Paging"],
    "concepts": ["Page table entry essential content"],
    "tags": ["page table", "page frame number"],
    "is_numerical": False,
    "formula_based": False,
    "estimated_solve_time_seconds": 30,
    "options": [
        {"label": "A", "text": "virtual page number", "is_correct": False},
        {"label": "B", "text": "page frame number", "is_correct": True},
        {"label": "C", "text": "both virtual page number and page frame number", "is_correct": False},
        {"label": "D", "text": "access right information", "is_correct": False}
    ],
    "correct_answer_text": None,
    "explanation": "Page frame numbers are most important; the virtual page number may not be stored entirely since it is implied by the page table entry's position/index.",
    "pyq_sources": [{"year": 2009, "set": 1, "question_number": "4.37", "marks": 1}]
})

add({
    "question_text": "A system uses FIFO policy for page replacement. It has 4 page frames with no pages loaded to begin with. The system first accesses 100 distinct pages in some order and then accesses the same 100 pages but now in reverse order. How many page faults will occur?",
    "question_type": "MCQ",
    "marks": 1,
    "difficulty": "hard",
    "topics": ["Page Replacement Algorithms"],
    "concepts": ["FIFO page replacement pattern"],
    "tags": ["fifo", "page faults", "reverse order access"],
    "is_numerical": True,
    "formula_based": True,
    "estimated_solve_time_seconds": 180,
    "options": [
        {"label": "A", "text": "196", "is_correct": True},
        {"label": "B", "text": "192", "is_correct": False},
        {"label": "C", "text": "197", "is_correct": False},
        {"label": "D", "text": "195", "is_correct": False}
    ],
    "correct_answer_text": None,
    "explanation": "For n distinct pages accessed forward then reverse with 4 frames using FIFO, the number of page faults follows the pattern 2n - 4. For n = 100, total page faults = 2(100) - 4 = 196.",
    "pyq_sources": [{"year": 2010, "set": 1, "question_number": "4.38", "marks": 1}]
})

add({
    "question_text": "Let the page fault service time be 10 ms in a computer with average memory access time being 20 ns. If one page fault is generated for every 10^6 memory accesses, what is the effective access time for the memory?",
    "question_type": "MCQ",
    "marks": 1,
    "difficulty": "medium",
    "topics": ["Demand Paging", "Effective Access Time"],
    "concepts": ["Effective access time with page fault rate"],
    "tags": ["effective access time", "page fault service time"],
    "is_numerical": True,
    "formula_based": True,
    "estimated_solve_time_seconds": 90,
    "options": [
        {"label": "A", "text": "21 ns", "is_correct": False},
        {"label": "B", "text": "30 ns", "is_correct": True},
        {"label": "C", "text": "23 ns", "is_correct": False},
        {"label": "D", "text": "35 ns", "is_correct": False}
    ],
    "correct_answer_text": None,
    "explanation": "Effective access time = (1-p) * access time when no page fault + p * access time during page fault = [1 - (1/10^6)] * 20 ns + (1/10^6) * 10 ms \u2248 30 ns.",
    "pyq_sources": [{"year": 2011, "set": 1, "question_number": "4.39", "marks": 1}]
})

add({
    "question_text": "Consider the virtual page reference string 1, 2, 3, 2, 4, 1, 3, 2, 4, 1 on a demand paged virtual memory system running on a computer system that has main memory size of 3 page frames which are initially empty. Let LRU, FIFO and OPTIMAL denote the number of page faults under the corresponding page replacement policy. Then",
    "question_type": "MCQ",
    "marks": 2,
    "difficulty": "medium",
    "topics": ["Page Replacement Algorithms"],
    "concepts": ["Comparing LRU, FIFO, Optimal page faults"],
    "tags": ["lru", "fifo", "optimal", "page faults comparison"],
    "is_numerical": True,
    "formula_based": False,
    "estimated_solve_time_seconds": 150,
    "options": [
        {"label": "A", "text": "OPTIMAL < LRU < FIFO", "is_correct": False},
        {"label": "B", "text": "OPTIMAL < FIFO < LRU", "is_correct": True},
        {"label": "C", "text": "OPTIMAL = LRU", "is_correct": False},
        {"label": "D", "text": "OPTIMAL = FIFO", "is_correct": False}
    ],
    "correct_answer_text": None,
    "explanation": "Tracing the reference string with 3 frames: Optimal gives 5 misses, FIFO gives 6 misses, LRU gives 9 misses. So OPTIMAL < FIFO < LRU.",
    "pyq_sources": [{"year": 2012, "set": None, "question_number": "4.40", "marks": 2}]
})

add({
    "question_text": "Linked Answer Questions 4.41 and 4.42: A computer uses 46-bit virtual address, 32-bit physical address, and a three-level paged page table organization. The page table base register stores the base address of the first-level (T1), which occupies exactly one page. Each entry of T1 stores the base address of a page of the second-level table (T2). Each entry of T2 stores the base address of a page of the third-level table (T3). Each entry of T3 stores a page table entry (PTE). The PTE is 32 bit in size. The processor used in the computer has a 1 MB 16-way-set associative virtually indexed physical tagged cache. The cache block size is 64 bytes. What is the size of a page in KB in this computer?",
    "question_type": "MCQ",
    "marks": 2,
    "difficulty": "hard",
    "topics": ["Multi-level Page Tables", "Virtual Memory"],
    "concepts": ["Three-level page table, page size derivation"],
    "tags": ["three-level paging", "page size", "virtual address"],
    "is_numerical": True,
    "formula_based": True,
    "estimated_solve_time_seconds": 180,
    "options": [
        {"label": "A", "text": "2", "is_correct": False},
        {"label": "B", "text": "4", "is_correct": False},
        {"label": "C", "text": "8", "is_correct": True},
        {"label": "D", "text": "16", "is_correct": False}
    ],
    "correct_answer_text": None,
    "explanation": "Since the third-level page table must fit into a single page, solving x^4 = 2^52 (where x is the page size) gives log2(x) = 13, so x = 2^13 = 8 KB.",
    "pyq_sources": [{"year": 2013, "set": None, "question_number": "4.41", "marks": 2}]
})

add({
    "question_text": "Linked Answer Questions 4.41 and 4.42 (same setup as Q4.41). What is the minimum number of page colours needed to guarantee that no two synonyms map to different sets in the processor cache of this computer?",
    "question_type": "MCQ",
    "marks": 2,
    "difficulty": "hard",
    "topics": ["Cache Memory"],
    "concepts": ["Page coloring", "virtually indexed physically tagged cache"],
    "tags": ["page coloring", "cache synonyms", "virtually indexed cache"],
    "is_numerical": True,
    "formula_based": True,
    "estimated_solve_time_seconds": 180,
    "options": [
        {"label": "A", "text": "2", "is_correct": False},
        {"label": "B", "text": "4", "is_correct": False},
        {"label": "C", "text": "8", "is_correct": True},
        {"label": "D", "text": "16", "is_correct": False}
    ],
    "correct_answer_text": None,
    "explanation": "Since the page size (8 KB = 2^13 bytes) exceeds what one cache line's set-index range can address without ambiguity, the number of colours needed = 2^13 / 2^10 = 2^3 = 8.",
    "pyq_sources": [{"year": 2013, "set": None, "question_number": "4.42", "marks": 2}]
})

add({
    "question_text": "Assume that there are 3 page frames which are initially empty. If the page reference string is 1, 2, 3, 4, 2, 1, 5, 3, 2, 4, 6, the number of page faults using the optimal replacement policy is ____.",
    "question_type": "NAT",
    "marks": 2,
    "difficulty": "medium",
    "topics": ["Page Replacement Algorithms"],
    "concepts": ["Optimal page replacement"],
    "tags": ["optimal replacement", "page faults", "nat"],
    "is_numerical": True,
    "formula_based": False,
    "estimated_solve_time_seconds": 150,
    "options": [],
    "correct_answer_text": "7",
    "explanation": "Tracing the reference string 1,2,3,4,2,1,5,3,2,4,6 with 3 frames using the optimal replacement policy gives 7 page faults.",
    "pyq_sources": [{"year": 2014, "set": 1, "question_number": "4.43", "marks": 2}]
})

add({
    "question_text": "A computer has twenty physical page frames which contain pages numbered 101 through 120. Now a program accesses the pages numbered 1, 2, ..., 100 in that order, and repeats the access sequence THRICE. Which one of the following page replacement policies experiences the same number of page faults as the optimal page replacement policy for this program?",
    "question_type": "MCQ",
    "marks": 2,
    "difficulty": "hard",
    "topics": ["Page Replacement Algorithms"],
    "concepts": ["MRU matching optimal in cyclic access pattern"],
    "tags": ["mru", "optimal replacement", "page faults", "cyclic access"],
    "is_numerical": True,
    "formula_based": False,
    "estimated_solve_time_seconds": 180,
    "options": [
        {"label": "A", "text": "Least-recently-used", "is_correct": False},
        {"label": "B", "text": "First-in-first-out", "is_correct": False},
        {"label": "C", "text": "Last-in-first-out", "is_correct": False},
        {"label": "D", "text": "Most-recently-used", "is_correct": True}
    ],
    "correct_answer_text": None,
    "explanation": "For this sequential and repeating access pattern with 20 frames, Most-Recently-Used replacement produces the same total of 260 page faults (100 for the first pass and 80 for each subsequent pass) as the optimal page replacement policy.",
    "pyq_sources": [{"year": 2014, "set": 2, "question_number": "4.44", "marks": 2}]
})

add({
    "question_text": "A system uses 3 page frames for storing process pages in main memory. It uses the Least Recently Used (LRU) page replacement policy. Assume that all the page frames are initially empty. What is the total number of page faults that will occur while processing the page reference string given below? 4, 7, 6, 1, 7, 6, 1, 2, 7, 2",
    "question_type": "NAT",
    "marks": 1,
    "difficulty": "medium",
    "topics": ["Page Replacement Algorithms"],
    "concepts": ["LRU page replacement"],
    "tags": ["lru", "page faults", "nat"],
    "is_numerical": True,
    "formula_based": False,
    "estimated_solve_time_seconds": 120,
    "options": [],
    "correct_answer_text": "6",
    "explanation": "Tracing the reference string 4,7,6,1,7,6,1,2,7,2 with 3 frames under LRU gives a total of 6 page faults.",
    "pyq_sources": [{"year": 2014, "set": 3, "question_number": "4.45", "marks": 1}]
})

add({
    "question_text": "Consider a paging hardware with a TLB. Assume that the entire page table and all the pages are in the physical memory. It takes 10 milliseconds to search the TLB and 80 milliseconds to access the physical memory. If the TLB hit ratio is 0.6, the effective memory access time (in milliseconds) is ____.",
    "question_type": "NAT",
    "marks": 2,
    "difficulty": "medium",
    "topics": ["TLB", "Effective Access Time"],
    "concepts": ["TLB hit ratio", "effective memory access time"],
    "tags": ["tlb", "effective access time", "nat"],
    "is_numerical": True,
    "formula_based": True,
    "estimated_solve_time_seconds": 120,
    "options": [],
    "correct_answer_text": "122",
    "explanation": "Effective Memory Access Time = H_TLB(T_TLB + T_M) + (1 - H_TLB)(T_TLB + T_M + T_M) = 0.6(10+80) + 0.4(10+80+80) = 0.6(90) + 0.4(170) = 122 ms.",
    "pyq_sources": [{"year": 2014, "set": 3, "question_number": "4.46", "marks": 2}]
})

add({
    "question_text": "Consider a system with byte-addressable memory, 32 bit logical addresses, 4 kilobyte page size and page table entries of 4 bytes each. The size of the page table in the system in megabytes is ____.",
    "question_type": "NAT",
    "marks": 1,
    "difficulty": "medium",
    "topics": ["Paging"],
    "concepts": ["Page table size calculation"],
    "tags": ["page table size", "paging", "nat"],
    "is_numerical": True,
    "formula_based": True,
    "estimated_solve_time_seconds": 90,
    "options": [],
    "correct_answer_text": "4",
    "explanation": "Page table size = number of page table entries x entry size = number of pages x 4 bytes = (2^32 / 2^12) x 4 bytes = 4 MB.",
    "pyq_sources": [{"year": 2015, "set": 1, "question_number": "4.47", "marks": 1}]
})

add({
    "question_text": "Consider a main memory with five page frames and the following sequence of page references: 3, 8, 2, 3, 9, 1, 6, 3, 8, 9, 3, 6, 2, 1, 3. Which one of the following is true with respect to page replacement policies First-In-First Out (FIFO) and Least Recently Used (LRU)?",
    "question_type": "MCQ",
    "marks": 2,
    "difficulty": "hard",
    "topics": ["Page Replacement Algorithms"],
    "concepts": ["Comparing FIFO and LRU page faults"],
    "tags": ["fifo", "lru", "page faults comparison"],
    "is_numerical": True,
    "formula_based": False,
    "estimated_solve_time_seconds": 180,
    "options": [
        {"label": "A", "text": "Both incur the same number of page faults", "is_correct": True},
        {"label": "B", "text": "FIFO incurs 2 more page faults than LRU", "is_correct": False},
        {"label": "C", "text": "LRU incurs 2 more page faults than FIFO", "is_correct": False},
        {"label": "D", "text": "LRU incurs 1 more page faults than FIFO", "is_correct": False}
    ],
    "correct_answer_text": None,
    "explanation": "Tracing the reference string with 5 frames: both FIFO and LRU incur 9 page faults, so both incur the same number of page faults.",
    "pyq_sources": [{"year": 2015, "set": 1, "question_number": "4.48", "marks": 2}]
})

add({
    "question_text": "A computer system implements a 40 bit virtual address, page size of 8 kilobytes, and a 128-entry translation look-aside buffer (TLB) organized into 32 sets each having four ways. Assume that the TLB tag does not store any process id. The minimum length of the TLB tag in bits is ____.",
    "question_type": "NAT",
    "marks": 1,
    "difficulty": "medium",
    "topics": ["TLB"],
    "concepts": ["Set-associative TLB tag sizing"],
    "tags": ["tlb", "tag bits", "nat"],
    "is_numerical": True,
    "formula_based": True,
    "estimated_solve_time_seconds": 120,
    "options": [],
    "correct_answer_text": "22",
    "explanation": "Page size = 8 KB = 2^13 bytes, so 13 bits for offset. Number of sets in TLB = 32, requiring 5 bits for set index. Out of 40-bit virtual address, 13 bits offset and 5 bits set index leave 40 - 13 - 5 = 22 bits for tag.",
    "pyq_sources": [{"year": 2015, "set": 2, "question_number": "4.49", "marks": 1}]
})

add({
    "question_text": "Consider six memory partitions of size 200 KB, 400 KB, 600 KB, 500 KB, 300 KB, and 250 KB, where KB refers to kilobyte. These partitions need to be allotted to four processes of sizes 357 KB, 210 KB, 468 KB and 491 KB in that order. If the best fit algorithm is used, which partitions are NOT allotted to any process?",
    "question_type": "MCQ",
    "marks": 2,
    "difficulty": "medium",
    "topics": ["Memory Allocation"],
    "concepts": ["Best-fit allocation strategy"],
    "tags": ["best-fit", "memory partitions", "allocation"],
    "is_numerical": True,
    "formula_based": False,
    "estimated_solve_time_seconds": 120,
    "options": [
        {"label": "A", "text": "200 KB and 300 KB", "is_correct": True},
        {"label": "B", "text": "200 KB and 250 KB", "is_correct": False},
        {"label": "C", "text": "250 KB and 300 KB", "is_correct": False},
        {"label": "D", "text": "300 KB and 400 KB", "is_correct": False}
    ],
    "correct_answer_text": None,
    "explanation": "The best-fit algorithm finds the smallest sufficient partition for each process: 357 KB->400 KB, 210 KB->250 KB, 468 KB->500 KB, 491 KB->600 KB. So partitions 200 KB and 300 KB are not allotted.",
    "pyq_sources": [{"year": 2015, "set": 2, "question_number": "4.50", "marks": 2}]
})

add({
    "question_text": "A Computer system implements 8 kilobyte pages and a 32-bit physical address space. Each page table entry contains a valid bit, a dirty bit, three permission bits, and the translation. If the maximum size of the page table of a process is 24 megabytes, the length of the virtual address supported by the system is ____ bits.",
    "question_type": "NAT",
    "marks": 2,
    "difficulty": "hard",
    "topics": ["Paging"],
    "concepts": ["Page table entry sizing", "virtual address length derivation"],
    "tags": ["page table entry", "virtual address length", "nat"],
    "is_numerical": True,
    "formula_based": True,
    "estimated_solve_time_seconds": 180,
    "options": [],
    "correct_answer_text": "36",
    "explanation": "Page size = 8 KB, giving 13 bits offset. Number of frame bits = 32 - 13 = 19. Page table entry = valid(1) + dirty(1) + permission(3) + translation(19) = 24 bits. Page table size = 24 MB, so number of pages = 24 MB / 24 bits = 2^23 pages, requiring 23 bits for the page number. Length of virtual address = 23 + 13 = 36 bits.",
    "pyq_sources": [{"year": 2015, "set": 2, "question_number": "4.51", "marks": 2}]
})

add({
    "question_text": "Consider a computer system with 40-bit virtual addressing and page size of sixteen kilobytes. If the computer system has a one-level page table per process and each page table entry requires 48 bits, then the size of the per-process page table is ____ megabytes.",
    "question_type": "NAT",
    "marks": 2,
    "difficulty": "medium",
    "topics": ["Paging"],
    "concepts": ["Page table size calculation"],
    "tags": ["page table size", "one-level page table", "nat"],
    "is_numerical": True,
    "formula_based": True,
    "estimated_solve_time_seconds": 120,
    "options": [],
    "correct_answer_text": "384",
    "explanation": "Page table size = number of entries in page table x page table entry size = (2^40 / 2^14) x 48 bits = 2^26 x 6 bytes = 64 M x 6 B = 384 MB.",
    "pyq_sources": [{"year": 2016, "set": 1, "question_number": "4.52", "marks": 2}]
})

add({
    "question_text": "Consider a computer system with ten physical page frames. The system is provided with an access sequence (a1, a2, ..., a20, a1, a2, ..., a20), where each ai is a distinct virtual page number. The difference in the number of page faults between the last-in-first-out (LIFO) page replacement policy and the optimal page replacement policy is ____.",
    "question_type": "NAT",
    "marks": 2,
    "difficulty": "hard",
    "topics": ["Page Replacement Algorithms"],
    "concepts": ["LIFO vs optimal page replacement"],
    "tags": ["lifo", "optimal replacement", "page faults", "nat"],
    "is_numerical": True,
    "formula_based": False,
    "estimated_solve_time_seconds": 180,
    "options": [],
    "correct_answer_text": "1",
    "explanation": "Using a smaller example (e.g., pages 1,2,3,4,1,2,3,4 with 2 frames) to establish the pattern, LIFO gives 7 page faults and optimal gives 6 page faults, so the difference is 7 - 6 = 1.",
    "pyq_sources": [{"year": 2016, "set": 1, "question_number": "4.53", "marks": 2}]
})

add({
    "question_text": "In which one of the following page replacement algorithms it is possible for the page fault rate to increase even when the number of allocated frames increases?",
    "question_type": "MCQ",
    "marks": 1,
    "difficulty": "easy",
    "topics": ["Belady's Anomaly", "Page Replacement Algorithms"],
    "concepts": ["Belady's anomaly"],
    "tags": ["belady's anomaly", "fifo", "page fault rate"],
    "is_numerical": False,
    "formula_based": False,
    "estimated_solve_time_seconds": 30,
    "options": [
        {"label": "A", "text": "LRU (Least Recently Used)", "is_correct": False},
        {"label": "B", "text": "OPT (Optimal Page Replacement)", "is_correct": False},
        {"label": "C", "text": "MRU (Most Recently Used)", "is_correct": False},
        {"label": "D", "text": "FIFO (First In First Out)", "is_correct": True}
    ],
    "correct_answer_text": None,
    "explanation": "Because of Belady's anomaly, this can happen with the FIFO page replacement algorithm.",
    "pyq_sources": [{"year": 2016, "set": 2, "question_number": "4.54", "marks": 1}]
})

add({
    "question_text": "Recall that Belady's anomaly is that the page-fault rate may increase as the number of allocated frames increases. Now, consider the following statements: S1: Random page replacement algorithm (where a page chosen at random is replaced) suffers from Belady's anomaly. S2: LRU page replacement algorithm suffers from Belady's anomaly. Which of the following is CORRECT?",
    "question_type": "MCQ",
    "marks": 2,
    "difficulty": "medium",
    "topics": ["Belady's Anomaly", "Page Replacement Algorithms"],
    "concepts": ["Random replacement vs LRU susceptibility to Belady's anomaly"],
    "tags": ["belady's anomaly", "random replacement", "lru"],
    "is_numerical": False,
    "formula_based": False,
    "estimated_solve_time_seconds": 90,
    "options": [
        {"label": "A", "text": "S1 is true, S2 is true", "is_correct": False},
        {"label": "B", "text": "S1 is true, S2 is false", "is_correct": True},
        {"label": "C", "text": "S1 is false, S2 is true", "is_correct": False},
        {"label": "D", "text": "S1 is false, S2 is false", "is_correct": False}
    ],
    "correct_answer_text": None,
    "explanation": "Random page replacement can behave like any algorithm, including FIFO, and hence can suffer from Belady's anomaly (S1 true). LRU is a stack algorithm and does not suffer from Belady's anomaly (S2 false).",
    "pyq_sources": [{"year": 2017, "set": 1, "question_number": "4.55", "marks": 2}]
})

add({
    "question_text": "Consider a process executing on an operating system that uses demand paging. The average time for a memory access in the system is M units if the corresponding memory page is available in memory and D units if the memory access causes a page fault. It has been experimentally measured that the average time taken for a memory access in the process is X units. Which one of the following is the correct expression for the page fault rate experienced by the process?",
    "question_type": "MCQ",
    "marks": 1,
    "difficulty": "medium",
    "topics": ["Demand Paging", "Effective Access Time"],
    "concepts": ["Deriving page fault rate from average access time"],
    "tags": ["demand paging", "page fault rate", "effective access time"],
    "is_numerical": True,
    "formula_based": True,
    "estimated_solve_time_seconds": 120,
    "options": [
        {"label": "A", "text": "(D - M) / (X - M)", "is_correct": False},
        {"label": "B", "text": "(X - M) / (D - M)", "is_correct": True},
        {"label": "C", "text": "(D - X) / (D - M)", "is_correct": False},
        {"label": "D", "text": "(X - M) / (D - X)", "is_correct": False}
    ],
    "correct_answer_text": None,
    "explanation": "EMAT = P x S + (1-P) x M, i.e., X = P x D + (1-P) x M. Rearranging: X - M = P(D - M), so P = (X-M)/(D-M).",
    "pyq_sources": [{"year": 2018, "set": None, "question_number": "4.56", "marks": 1}]
})

add({
    "question_text": "Assume that in a certain computer, the virtual addresses are 64 bits long and the physical addresses are 48 bits long. The memory is word addressable. The page size is 8 kB and the word size is 4 bytes. The Translation Look-aside Buffer (TLB) in the address translation path has 128 valid entries. At most how many distinct virtual addresses can be translated without any TLB miss?",
    "question_type": "MCQ",
    "marks": 2,
    "difficulty": "hard",
    "topics": ["TLB"],
    "concepts": ["TLB reach", "word-addressable memory"],
    "tags": ["tlb", "tlb reach", "word addressable"],
    "is_numerical": True,
    "formula_based": True,
    "estimated_solve_time_seconds": 180,
    "options": [
        {"label": "A", "text": "16 x 2^10", "is_correct": False},
        {"label": "B", "text": "8 x 2^20", "is_correct": False},
        {"label": "C", "text": "4 x 2^20", "is_correct": False},
        {"label": "D", "text": "256 x 2^10", "is_correct": True}
    ],
    "correct_answer_text": None,
    "explanation": "Number of words in 1 page = page size / word size = 2^13 / 2^2 = 2^11. TLB can hold 128 valid entries, so at most 128 x 2^11 = 256 x 2^10 memory addresses can be addressed without a TLB miss.",
    "pyq_sources": [{"year": 2019, "set": None, "question_number": "4.57", "marks": 2}]
})

add({
    "question_text": "Consider allocation of memory to a new process. Assume that none of the existing holes in the memory will exactly fit the process's memory requirement. Hence, a new hole of smaller size will be created if allocation is made in any of the existing holes. Which one of the following statements is TRUE?",
    "question_type": "MCQ",
    "marks": 1,
    "difficulty": "hard",
    "topics": ["Memory Allocation"],
    "concepts": ["Best-fit vs first-fit vs next-fit vs worst-fit hole comparison"],
    "tags": ["best-fit", "first-fit", "next-fit", "worst-fit"],
    "is_numerical": False,
    "formula_based": False,
    "estimated_solve_time_seconds": 120,
    "options": [
        {"label": "A", "text": "The hole created by next fit is never larger than the hole created by best fit.", "is_correct": False},
        {"label": "B", "text": "The hole created by first fit is always larger than the hole created by next fit.", "is_correct": False},
        {"label": "C", "text": "The hole created by best fit is never larger than the hole created by first fit.", "is_correct": True},
        {"label": "D", "text": "The hole created by worst fit is always larger than the hole created by first fit.", "is_correct": False}
    ],
    "correct_answer_text": None,
    "explanation": "The hole created by best fit is never larger than the hole created by first fit, since best fit always chooses the smallest sufficient hole, leaving the smallest possible remainder.",
    "pyq_sources": [{"year": 2020, "set": None, "question_number": "4.58", "marks": 1}]
})

add({
    "question_text": "Consider a paging system that uses 1-level page table residing in main memory and a TLB for address translation. Each main memory access takes 100 ns and TLB lookup takes 20 ns. Each page transfer to/from the disk takes 5000 ns. Assume that the TLB hit ratio is 95%, page fault rate is 10%. Assume that for 20% of the total page faults, a dirty page has to be written back to disk before the required page is read in from disk. TLB update time is negligible. The average memory access time in ns (round off to 1 decimal places) is ____.",
    "question_type": "NAT",
    "marks": 2,
    "difficulty": "hard",
    "topics": ["TLB", "Demand Paging", "Effective Access Time"],
    "concepts": ["EMAT with TLB, page faults, and dirty page write-back"],
    "tags": ["tlb", "page fault", "dirty page", "average access time", "nat"],
    "is_numerical": True,
    "formula_based": True,
    "estimated_solve_time_seconds": 240,
    "options": [],
    "correct_answer_text": "154.5",
    "explanation": "EMAT = 0.95 x (20+100) + 0.05 x (0.9 x (20+100+100) + 0.1 x [0.2 x (20+100+5000+5000) + 0.8 x (20+100+5000)]) = 154.5 ns.",
    "pyq_sources": [{"year": 2020, "set": None, "question_number": "4.59", "marks": 2}]
})

add({
    "question_text": "In the context of operating systems, which of the following statements is/are correct with respect to paging? (a) Paging incurs memory overheads. (b) Multi-level paging is necessary to support pages of different sizes. (c) Page size has no impact on internal fragmentation. (d) Paging helps solve the issue of external fragmentation.",
    "question_type": "MSQ",
    "marks": 1,
    "difficulty": "medium",
    "topics": ["Paging", "Fragmentation"],
    "concepts": ["Paging overheads", "internal vs external fragmentation"],
    "tags": ["paging", "fragmentation", "memory overhead"],
    "is_numerical": False,
    "formula_based": False,
    "estimated_solve_time_seconds": 90,
    "options": [
        {"label": "A", "text": "Paging incurs memory overheads.", "is_correct": True},
        {"label": "B", "text": "Multi-level paging is necessary to support pages of different sizes.", "is_correct": False},
        {"label": "C", "text": "Page size has no impact on internal fragmentation.", "is_correct": False},
        {"label": "D", "text": "Paging helps solve the issue of external fragmentation.", "is_correct": True}
    ],
    "correct_answer_text": None,
    "explanation": "Paging incurs memory overheads (page tables) and helps solve external fragmentation since memory is allocated in fixed-size frames; it does not eliminate internal fragmentation, and multi-level paging is used to reduce page table overhead, not to support pages of different sizes.",
    "pyq_sources": [{"year": 2021, "set": 1, "question_number": "4.60", "marks": 1}]
})

add({
    "question_text": "Consider a three-level page table to translate a 39-bit virtual address to a physical address, structured as: Level 1 offset (9 bits), Level 2 offset (9 bits), Level 3 offset (9 bits), Page offset (12 bits). The page size is 4 KB (1 KB = 2^10 bytes) and page table entry size at every level is 8 bytes. A process P is currently using 2 GB (1 GB = 2^30 bytes) virtual memory which is mapped to 2 GB of physical memory. The minimum amount of memory required for the page table of P across all levels is ____ KB.",
    "question_type": "NAT",
    "marks": 2,
    "difficulty": "hard",
    "topics": ["Multi-level Page Tables"],
    "concepts": ["Three-level page table sizing across levels"],
    "tags": ["three-level paging", "page table size", "nat"],
    "is_numerical": True,
    "formula_based": True,
    "estimated_solve_time_seconds": 240,
    "options": [],
    "correct_answer_text": "4108",
    "explanation": "Number of pages used = 2^31 / 2^12 = 2^19. Number of 3rd-level page tables needed = 2^19 / 2^9 = 2^10. Number of 2nd-level page tables needed = 2^10 / 2^9 = 2. Number of 1st-level page tables needed = 1. Total page tables = 2^10 + 2 + 1 = 1027. Total size = 1027 x 2^9 x 8 bytes = 4108 KB.",
    "pyq_sources": [{"year": 2021, "set": 1, "question_number": "4.61", "marks": 2}]
})

add({
    "question_text": "Which one of the following statements is FALSE? (a) The TLB performs an associative search in parallel on all its valid entries using page number of incoming virtual address. (b) If the virtual address of a word given by CPU has a TLB hit, but the subsequent search for the word results in a cache miss, then the word will always be present in the main memory. (c) The memory access time using a given inverted page table is always same for all incoming virtual addresses. (d) In a system that uses hashed page tables, if two distinct virtual addresses V1 and V2 map to the same value while hashing, then the memory access time of these addresses will not be the same.",
    "question_type": "MCQ",
    "marks": 2,
    "difficulty": "hard",
    "topics": ["TLB", "Inverted and Hashed Page Tables"],
    "concepts": ["TLB associative search", "inverted page table access time", "hashed page table collisions"],
    "tags": ["tlb", "inverted page table", "hashed page table"],
    "is_numerical": False,
    "formula_based": False,
    "estimated_solve_time_seconds": 150,
    "options": [
        {"label": "A", "text": "The TLB performs an associative search in parallel on all its valid entries using page number of incoming virtual address.", "is_correct": False},
        {"label": "B", "text": "If the virtual address of a word given by CPU has a TLB hit, but the subsequent search for the word results in a cache miss, then the word will always be present in the main memory.", "is_correct": False},
        {"label": "C", "text": "The memory access time using a given inverted page table is always same for all incoming virtual addresses.", "is_correct": True},
        {"label": "D", "text": "In a system that uses hashed page tables, if two distinct virtual addresses V1 and V2 map to the same value while hashing, then the memory access time of these addresses will not be the same.", "is_correct": False}
    ],
    "correct_answer_text": None,
    "explanation": "Statement (c) is false because memory access time using an inverted page table is not always the same for all incoming virtual addresses, since there is no direct indexing and a linear/hashed search is followed instead.",
    "pyq_sources": [{"year": 2022, "set": None, "question_number": "4.62", "marks": 2}]
})

add({
    "question_text": "Consider a demand paging system with four page frames (initially empty) and LRU page replacement policy. For the following page reference string: 7, 2, 7, 3, 2, 5, 3, 4, 6, 7, 7, 1, 5, 6, 1, the page fault rate, defined as the ratio of number of page faults to the number of memory accesses (rounded off to one decimal place) is ____.",
    "question_type": "NAT",
    "marks": 2,
    "difficulty": "medium",
    "topics": ["Page Replacement Algorithms"],
    "concepts": ["LRU page replacement", "page fault rate"],
    "tags": ["lru", "page fault rate", "nat"],
    "is_numerical": True,
    "formula_based": True,
    "estimated_solve_time_seconds": 150,
    "options": [],
    "correct_answer_text": "0.6",
    "explanation": "Tracing the reference string with 4 frames under LRU gives 9 page faults out of a total of 15 references, so the page fault rate = 9/15 = 0.6.",
    "pyq_sources": [{"year": 2022, "set": None, "question_number": "4.63", "marks": 2}]
})

add({
    "question_text": "Consider the following two-dimensional array D in the C programming language, which is stored in row-major order: int D[128][128]; Demand paging is used for allocating memory and each physical page frame holds 512 elements of the array D. The Least Recently Used (LRU) page-replacement policy is used by the operating system. A total of 30 physical page frames are allocated to a process which executes the following code snippet: for (int i = 0; i < 128; i++) for (int j = 0; j < 128; j++) D[j][i] *= 10; The number of page faults generated during the execution of this code snippet is ____.",
    "question_type": "NAT",
    "marks": 2,
    "difficulty": "hard",
    "topics": ["Demand Paging", "Page Replacement Algorithms"],
    "concepts": ["Row-major storage vs column-major access", "LRU page faults"],
    "tags": ["demand paging", "row-major order", "lru", "nat"],
    "is_numerical": True,
    "formula_based": True,
    "estimated_solve_time_seconds": 240,
    "options": [],
    "correct_answer_text": "4096",
    "explanation": "The array is stored in row-major order and accessed in column-major order, so consecutive accesses jump across pages. The array spans 32 pages, but memory has only 30 frames, so essentially every group of accesses causes a fault: total page faults = (128 x 128) / 4 = 2^14 = 4096.",
    "pyq_sources": [{"year": 2023, "set": None, "question_number": "4.64", "marks": 2}]
})

add({
    "question_text": "Consider a computer system with 57-bit virtual addressing using multi-level tree-structured page tables for virtual to physical address translation. The page size is 4 KB (1 KB = 1024 B) and a page table entry at any of the levels occupies 8 bytes. The value of L is ____.",
    "question_type": "NAT",
    "marks": 2,
    "difficulty": "medium",
    "topics": ["Multi-level Page Tables"],
    "concepts": ["Number of levels in multi-level page table"],
    "tags": ["multi-level paging", "page table levels", "nat"],
    "is_numerical": True,
    "formula_based": True,
    "estimated_solve_time_seconds": 150,
    "options": [],
    "correct_answer_text": "5",
    "explanation": "Offset = log2(4 KB) = 12 bits. Since a page table entry is 8 bytes, number of entries per page = 4KB / 8B = 2^9, requiring 9 bits per level. Remaining bits for levels = 57 - 12 = 45 bits, so number of levels L = 45 / 9 = 5.",
    "pyq_sources": [{"year": 2023, "set": None, "question_number": "4.65", "marks": 2}]
})

add({
    "question_text": "Consider a memory management system that uses a page size of 2 KB. Assume that both the physical and virtual addresses start from 0. Assume that the pages 0, 1, 2, and 3 are stored in the page frames 1, 3, 2, and 0, respectively. The physical address (in decimal format) corresponding to the virtual address 2500 (in decimal format) is ____.",
    "question_type": "NAT",
    "marks": 2,
    "difficulty": "medium",
    "topics": ["Paging"],
    "concepts": ["Virtual to physical address translation"],
    "tags": ["paging", "address translation", "nat"],
    "is_numerical": True,
    "formula_based": True,
    "estimated_solve_time_seconds": 120,
    "options": [],
    "correct_answer_text": "6596",
    "explanation": "Virtual address 2500 in binary corresponds to page 1 with a certain offset; mapping page 1 to frame 3 and combining with the offset gives a physical address of (1100111000100)2 = 6596 in decimal.",
    "pyq_sources": [{"year": 2024, "set": 1, "question_number": "4.66", "marks": 2}]
})

add({
    "question_text": "Which of the following tasks is/are the responsibility/responsibilities of the memory management unit (MMU) in a system with paging-based memory management? (a) Allocate a new page table for a newly created process. (b) Translate a virtual address to a physical address using the page table. (c) Raise a trap when a process tries to write to a page marked with read-only permission in the page table. (d) Raise a trap when a virtual address is not found in the page table.",
    "question_type": "MSQ",
    "marks": 1,
    "difficulty": "medium",
    "topics": ["Memory Management Unit", "Paging"],
    "concepts": ["MMU responsibilities"],
    "tags": ["mmu", "page table", "address translation", "trap"],
    "is_numerical": False,
    "formula_based": False,
    "estimated_solve_time_seconds": 90,
    "options": [
        {"label": "A", "text": "Allocate a new page table for a newly created process.", "is_correct": False},
        {"label": "B", "text": "Translate a virtual address to a physical address using the page table.", "is_correct": True},
        {"label": "C", "text": "Raise a trap when a process tries to write to a page marked with read-only permission in the page table.", "is_correct": True},
        {"label": "D", "text": "Raise a trap when a virtual address is not found in the page table.", "is_correct": True}
    ],
    "correct_answer_text": None,
    "explanation": "The MMU is responsible for translating virtual to physical addresses and raising traps for protection violations or page faults. Allocating a new page table for a newly created process is an operating system responsibility, not the MMU's.",
    "pyq_sources": [{"year": 2024, "set": 2, "question_number": "4.67", "marks": 1}]
})

add({
    "question_text": "Consider a 32-bit system with 4 KB page size and page table entries of size 4 bytes each. Assume 1 KB = 2^10 bytes. The OS uses a 2-level page table for memory management, with the page table containing an outer page directory and an inner page table. The OS allocates a page for the outer page directory upon process creation. The OS uses demand paging when allocating memory for the inner page table, i.e., a page of the inner page table is allocated only if it contains at least one valid page table entry. An active process in this system accesses 2000 unique pages during its execution, and none of the pages are swapped out to disk. After it completes the page accesses, let X denote the minimum and Y denote the maximum number of pages across the two levels of the page table of the process. The value of X + Y is ____.",
    "question_type": "NAT",
    "marks": 2,
    "difficulty": "hard",
    "topics": ["Multi-level Page Tables", "Demand Paging"],
    "concepts": ["Demand-allocated inner page tables", "min/max page table pages"],
    "tags": ["two-level paging", "demand paging", "page directory", "nat"],
    "is_numerical": True,
    "formula_based": True,
    "estimated_solve_time_seconds": 240,
    "options": [],
    "correct_answer_text": "1028",
    "explanation": "With a 4 KB page and 4-byte entries, each inner page table has 1024 entries, covering 1024 unique pages per inner page table page. To cover 2000 unique pages, the minimum number of inner page table pages needed is 2 (if references are contiguous) and the maximum is 2000 (if references are maximally scattered, one per inner page). Including the 1 outer page directory page: X (minimum total) = 1 + 2 = 3 and Y (maximum total) = 1 + ... ; combining the outer directory page across both levels, X + Y = 1028.",
    "pyq_sources": [{"year": 2024, "set": 2, "question_number": "4.68", "marks": 2}]
})

add({
    "question_text": "Consider a demand paging memory management system with 32-bit logical address, 20-bit physical address, and page size of 2048 bytes. Assuming that the memory is byte addressable, what is the maximum number of entries in the page table?",
    "question_type": "MCQ",
    "marks": 1,
    "difficulty": "medium",
    "topics": ["Paging"],
    "concepts": ["Number of page table entries derivation"],
    "tags": ["page table entries", "paging", "logical address"],
    "is_numerical": True,
    "formula_based": True,
    "estimated_solve_time_seconds": 90,
    "options": [
        {"label": "A", "text": "2^21", "is_correct": True},
        {"label": "B", "text": "2^20", "is_correct": False},
        {"label": "C", "text": "2^22", "is_correct": False},
        {"label": "D", "text": "2^24", "is_correct": False}
    ],
    "correct_answer_text": None,
    "explanation": "Number of entries in page table = Logical Address Space / Page size = 2^32 B / 2^11 B = 2^21.",
    "pyq_sources": [{"year": 2025, "set": 1, "question_number": "4.69", "marks": 1}]
})

add({
    "question_text": "In optimal page replacement algorithm, information about all future page references is available to the operating system (OS). A modification of the optimal page replacement algorithm is as follows: The OS correctly predicts only up to next 4 page references (including the current page) at the time of allocating a frame to a page. A process accesses the pages in the following order of page numbers: 1, 3, 2, 4, 2, 3, 1, 2, 4, 3, 1, 4. If the system has three memory frames that are initially empty, the number of page faults that will occur during execution of the process is ____. (Answer in integer)",
    "question_type": "NAT",
    "marks": 2,
    "difficulty": "hard",
    "topics": ["Page Replacement Algorithms"],
    "concepts": ["Modified optimal page replacement with limited lookahead"],
    "tags": ["optimal replacement", "lookahead", "page faults", "nat"],
    "is_numerical": True,
    "formula_based": False,
    "estimated_solve_time_seconds": 240,
    "options": [],
    "correct_answer_text": "6",
    "explanation": "Tracing the reference string 1,3,2,4,2,3,1,2,4,3,1,4 with 3 frames using the optimal replacement policy limited to a 4-reference lookahead window gives a total of 6 page faults.",
    "pyq_sources": [{"year": 2025, "set": 1, "question_number": "4.70", "marks": 2}]
})

add({
    "question_text": "Consider a demand paging system with three frames, and the following page reference string: 1 2 3 4 5 4 1 6 4 5 1 3 2. The contents of the frames are as follows initially and after each reference (from left to right), with *-marked references causing page replacements. Which one or more of the following could be the page replacement policy/policies in use? (a) Least Recently Used page replacement policy (b) Least Frequently Used page replacement policy (c) Most Frequently Used page replacement policy (d) Optimal page replacement policy",
    "question_type": "MSQ",
    "marks": 2,
    "difficulty": "hard",
    "topics": ["Page Replacement Algorithms"],
    "concepts": ["Identifying replacement policy from frame trace"],
    "tags": ["lru", "lfu", "mfu", "optimal replacement"],
    "is_numerical": False,
    "formula_based": False,
    "estimated_solve_time_seconds": 240,
    "options": [
        {"label": "A", "text": "Least Recently Used page replacement policy", "is_correct": False},
        {"label": "B", "text": "Least Frequently Used page replacement policy", "is_correct": False},
        {"label": "C", "text": "Most Frequently Used page replacement policy", "is_correct": False},
        {"label": "D", "text": "Optimal page replacement policy", "is_correct": True}
    ],
    "correct_answer_text": None,
    "explanation": "Comparing the given frame trace against each candidate policy, only the Optimal page replacement policy is consistent with the observed replacements marked in the trace.",
    "pyq_sources": [{"year": 2025, "set": 2, "question_number": "4.71", "marks": 2}]
})

add({
    "question_text": "A computer system supports a logical address space of 2^32 bytes. It uses two-level hierarchical paging with a page size of 4096 bytes. A logical address is divided into a b-bit index to the outer page table, an offset within the page of the inner page table, and an offset within the desired page. Each entry of the inner page table uses eight bytes. All the pages in the system have the same size. The value of b is ____. (Answer in integer)",
    "question_type": "NAT",
    "marks": 2,
    "difficulty": "hard",
    "topics": ["Multi-level Page Tables"],
    "concepts": ["Two-level hierarchical paging index sizing"],
    "tags": ["two-level paging", "outer page table", "nat"],
    "is_numerical": True,
    "formula_based": True,
    "estimated_solve_time_seconds": 180,
    "options": [],
    "correct_answer_text": "11",
    "explanation": "Logical address space = 2^32 bits, page size = 4096 bytes = 2^12 bytes, so offset within page = 12 bits and remaining 20 bits are split between the outer index (b bits) and inner page offset. Each inner page table entry is 8 bytes, so a 4096-byte page of the inner table holds 4096/8 = 2^9 entries, needing 9 bits for the inner page offset. Therefore b = 20 - 9 = 11 bits.",
    "pyq_sources": [{"year": 2025, "set": 2, "question_number": "4.72", "marks": 2}]
})

add({
    "question_text": "Consider a system that has a cache memory unit and a memory management unit (MMU). The address input to the cache memory is a physical address. The MMU has a translation lookaside buffer (TLB). Assume that when a page is evicted from the main memory, the corresponding blocks in the cache are marked as invalid. For a given memory reference, which of the following sequences of events can NEVER happen? (a) TLB miss, Page table hit, Cache hit (b) TLB hit, Page table miss, Cache hit (c) TLB miss, Page table miss, Cache hit (d) TLB miss, Page table miss, Cache miss",
    "question_type": "MSQ",
    "marks": 2,
    "difficulty": "hard",
    "topics": ["TLB", "Cache Memory"],
    "concepts": ["Consistency between TLB, page table, and physically-indexed cache states"],
    "tags": ["tlb", "cache", "page table", "physically indexed cache"],
    "is_numerical": False,
    "formula_based": False,
    "estimated_solve_time_seconds": 240,
    "options": [
        {"label": "A", "text": "TLB miss, Page table hit, Cache hit", "is_correct": False},
        {"label": "B", "text": "TLB hit, Page table miss, Cache hit", "is_correct": True},
        {"label": "C", "text": "TLB miss, Page table miss, Cache hit", "is_correct": True},
        {"label": "D", "text": "TLB miss, Page table miss, Cache miss", "is_correct": False}
    ],
    "correct_answer_text": None,
    "explanation": "(a) is possible since a TLB miss can still be followed by a page table hit and cache hit (cache uses physical address). (b) is impossible since a TLB hit means the translation is already available, so the page table would not need to be consulted, making a page table miss logically inconsistent. (c) is impossible since a page table miss means a page fault (page not in main memory), so the cache, which holds only valid blocks of pages present in memory, cannot have a hit. (d) is possible since a TLB miss and page table miss (page fault) naturally leads to a cache miss as well.",
    "pyq_sources": [{"year": 2026, "set": 1, "question_number": "4.73", "marks": 2}]
})

add({
    "question_text": "A system has a Translation Lookaside Buffer (TLB) that has a reach of 1 MB. TLB reach is defined as the total amount of physical memory that can be accessed through the TLB entries. The paging system uses pages of size 4 KB. The virtual address space is 64 GB and physical address space is 1 GB. If each TLB entry stores a 4-bit process id, page number, frame number, and a 2-bit control field, then the size of the TLB (in bytes) is ____. (answer in integer) Note: 1K=2^10, 1M=2^20, 1G=2^30",
    "question_type": "NAT",
    "marks": 2,
    "difficulty": "hard",
    "topics": ["TLB"],
    "concepts": ["TLB reach", "TLB entry sizing", "TLB size calculation"],
    "tags": ["tlb reach", "tlb entry", "tlb size", "nat"],
    "is_numerical": True,
    "formula_based": True,
    "estimated_solve_time_seconds": 240,
    "options": [],
    "correct_answer_text": "1536",
    "explanation": "Number of TLB entries = TLB reach / page size = 1 MB / 4 KB = 2^20/2^12 = 2^8 = 256. Number of pages = virtual address space / page size = 64 GB / 4 KB = 2^36/2^12 = 2^24, so page number needs 24 bits. Number of frames = physical address space / frame size = 2^30/2^12 = 2^18, so frame number needs 18 bits. TLB entry bits = process id (4) + page number (24) + frame number (18) + control bits (2) = 48 bits. TLB size = 256 x 48 bits / 8 = 1536 bytes.",
    "pyq_sources": [{"year": 2026, "set": 2, "question_number": "4.74", "marks": 2}]
})

add({
    "question_text": "Consider contiguous allocation of physical memory to processes using variable partitioning scheme. Suppose there are 8 holes in the memory of sizes 20 KB, 4 KB, 25 KB, 18 KB, 7 KB, 9 KB, 15 KB, and 12 KB. Assume that no two holes are adjacent. Two processes P1 of size 16 KB and P2 of size 9 KB arrive in that order, and they are allocated memory using the best-fit technique. After allocating space to P1 and P2, the number of holes of size less than 8 KB is ____. (answer in integer) Note: 1K=2^10",
    "question_type": "NAT",
    "marks": 2,
    "difficulty": "medium",
    "topics": ["Memory Allocation"],
    "concepts": ["Best-fit allocation with resulting hole sizes"],
    "tags": ["best-fit", "variable partitioning", "holes", "nat"],
    "is_numerical": True,
    "formula_based": False,
    "estimated_solve_time_seconds": 180,
    "options": [],
    "correct_answer_text": "3",
    "explanation": "For P1 (16 KB), best fit selects the 18 KB hole (smallest sufficient), leaving a 2 KB hole. For P2 (9 KB), best fit selects the 9 KB hole exactly, leaving no hole. After both allocations, holes smaller than 8 KB are: 4 KB, 2 KB (remainder), and 7 KB, giving a total of 3.",
    "pyq_sources": [{"year": 2026, "set": 2, "question_number": "4.75", "marks": 2}]
})

result = {
    "subject": subject,
    "topics": topics,
    "questions": questions
}

with open("gate_os_memory_management.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print("Total questions:", len(questions))
print("JSON written successfully")