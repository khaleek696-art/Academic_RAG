import os
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Target Directory
OUTPUT_DIR = Path("data/sample")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
PDF_PATH = OUTPUT_DIR / "Operating_Systems_Chapter1_Process_Management.pdf"

def generate_academic_pdf():
    doc = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=letter,
        rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Styling
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#1E3A8A'),
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'Heading1Custom',
        parent=styles['Heading2'],
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#2563EB'),
        spaceBefore=14,
        spaceAfter=8
    )

    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontSize=10.5,
        leading=15,
        textColor=colors.HexColor('#1F2937'),
        spaceAfter=10
    )

    bullet_style = ParagraphStyle(
        'BulletCustom',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        leftIndent=15,
        spaceAfter=6
    )

    story = []

    # ---------------- PAGE 1 ----------------
    story.append(Paragraph("📚 Chapter 1: Introduction to Operating Systems", title_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563EB'), spaceAfter=15))

    story.append(Paragraph("1.1 Definition & Overview", h1_style))
    story.append(Paragraph(
        "An <b>Operating System (OS)</b> is system software that manages computer hardware, software resources, and provides common services for computer programs. "
        "It acts as an intermediary interface between computer hardware and the user applications.",
        body_style
    ))

    story.append(Paragraph("1.2 Core Functions of an OS", h1_style))
    story.append(Paragraph("• <b>Process Management</b>: Creation, scheduling, and termination of active processes.", bullet_style))
    story.append(Paragraph("• <b>Memory Management</b>: Allocation and deallocation of main memory (RAM) space.", bullet_style))
    story.append(Paragraph("• <b>File System Management</b>: Organization, storage, retrieval, and access control of files.", bullet_style))
    story.append(Paragraph("• <b>Device Management</b>: Coordinating I/O devices via hardware drivers.", bullet_style))

    story.append(Paragraph("1.3 Monolithic Kernel vs Microkernel", h1_style))
    story.append(Paragraph(
        "In a <b>Monolithic Kernel</b>, all system components such as the file system, memory manager, device drivers, and IPC run in kernel mode within a single address space. "
        "In contrast, a <b>Microkernel</b> keeps only core services (like IPC and basic scheduling) in kernel mode, while running drivers and file systems in user mode.",
        body_style
    ))
    story.append(PageBreak())

    # ---------------- PAGE 2 ----------------
    story.append(Paragraph("📚 Chapter 2: Process Management & PCB", title_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563EB'), spaceAfter=15))

    story.append(Paragraph("2.1 What is a Process?", h1_style))
    story.append(Paragraph(
        "A <b>Process</b> is a program in execution. Unlike a program which is a passive entity stored on disk, a process is an active entity loaded into RAM with a program counter, registers, and stack.",
        body_style
    ))

    story.append(Paragraph("2.2 Process Control Block (PCB)", h1_style))
    story.append(Paragraph(
        "The kernel maintains a data structure for every process called the <b>Process Control Block (PCB)</b>. Key attributes stored in a PCB include:",
        body_style
    ))
    story.append(Paragraph("• <b>Process ID (PID)</b>: Unique numerical identifier for the process.", bullet_style))
    story.append(Paragraph("• <b>Process State</b>: Current state (New, Ready, Running, Waiting, Terminated).", bullet_style))
    story.append(Paragraph("• <b>Program Counter (PC)</b>: Address of the next instruction to execute.", bullet_style))
    story.append(Paragraph("• <b>CPU Registers</b>: Accumulators, index registers, and stack pointers saved during context switches.", bullet_style))
    story.append(Paragraph("• <b>CPU Scheduling Info</b>: Process priority and queue pointers.", bullet_style))

    story.append(Paragraph("2.3 Five States of a Process", h1_style))
    story.append(Paragraph("1. <b>New</b>: The process is being created.", bullet_style))
    story.append(Paragraph("2. <b>Ready</b>: The process is waiting to be assigned to a CPU core.", bullet_style))
    story.append(Paragraph("3. <b>Running</b>: Instructions are currently being executed by the CPU.", bullet_style))
    story.append(Paragraph("4. <b>Waiting (Blocked)</b>: The process is waiting for an I/O event or signal.", bullet_style))
    story.append(Paragraph("5. <b>Terminated</b>: The process has finished execution.", bullet_style))
    story.append(PageBreak())

    # ---------------- PAGE 3 ----------------
    story.append(Paragraph("📚 Chapter 3: Process Synchronization & Semaphores", title_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563EB'), spaceAfter=15))

    story.append(Paragraph("3.1 The Critical Section Problem", h1_style))
    story.append(Paragraph(
        "When multiple concurrent processes share global data, a <b>Race Condition</b> can occur if execution order alters the outcome. "
        "A <b>Critical Section</b> is a code segment where shared variables or files are accessed.",
        body_style
    ))
    story.append(Paragraph("To solve the Critical Section Problem, any synchronization solution must satisfy three requirements:", body_style))
    story.append(Paragraph("1. <b>Mutual Exclusion</b>: If process P is executing in its critical section, no other process can enter.", bullet_style))
    story.append(Paragraph("2. <b>Progress</b>: If no process is executing in its critical section, selection of next process cannot be postponed indefinitely.", bullet_style))
    story.append(Paragraph("3. <b>Bounded Waiting</b>: There must be a limit on the number of times other processes enter critical section after a request is made.", bullet_style))

    story.append(Paragraph("3.2 Semaphores: Counting vs Binary", h1_style))
    story.append(Paragraph(
        "A <b>Semaphore</b> is an integer variable accessed only through atomic operations: <code>wait()</code> (P operation) and <code>signal()</code> (V operation).",
        body_style
    ))
    story.append(Paragraph("• <b>Counting Semaphore</b>: Value ranges over an unrestricted domain, used for resource allocation with finite instances.", bullet_style))
    story.append(Paragraph("• <b>Binary Semaphore (Mutex)</b>: Value ranges only between 0 and 1, used primarily for mutual exclusion locks.", bullet_style))
    story.append(PageBreak())

    # ---------------- PAGE 4 ----------------
    story.append(Paragraph("📚 Chapter 4: CPU Scheduling Algorithms", title_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563EB'), spaceAfter=15))

    story.append(Paragraph("4.1 CPU Scheduler Overview", h1_style))
    story.append(Paragraph(
        "The <b>CPU Scheduler</b> selects a process from the ready queue and allocates the CPU. "
        "Primary metrics include CPU Utilization, Throughput, Turnaround Time, Waiting Time, and Response Time.",
        body_style
    ))

    story.append(Paragraph("4.2 Common CPU Scheduling Algorithms", h1_style))
    story.append(Paragraph(
        "<b>1. First-Come, First-Served (FCFS)</b>: Non-preemptive algorithm. Simple FIFO queue. Suffers from the <i>Convoy Effect</i> where short processes wait behind long ones.",
        body_style
    ))
    story.append(Paragraph(
        "<b>2. Shortest Job First (SJF)</b>: Associates CPU burst length with each process. Gives optimal minimum average waiting time. Preemptive version is called <i>SRTF (Shortest Remaining Time First)</i>.",
        body_style
    ))
    story.append(Paragraph(
        "<b>3. Round Robin (RR)</b>: Designed for time-sharing systems. Each process gets a fixed unit of time called a <b>Time Quantum (q)</b> (typically 10-100 ms). Preemptive.",
        body_style
    ))
    story.append(Paragraph(
        "<b>4. Priority Scheduling</b>: CPU allocated to highest priority process. Can suffer from <i>Starvation</i>, which is resolved using <b>Aging</b> (gradually increasing process priority over time).",
        body_style
    ))
    story.append(PageBreak())

    # ---------------- PAGE 5 ----------------
    story.append(Paragraph("📚 Chapter 5: Deadlocks & Banker's Algorithm", title_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563EB'), spaceAfter=15))

    story.append(Paragraph("5.1 What is a Deadlock?", h1_style))
    story.append(Paragraph(
        "A <b>Deadlock</b> is a situation where a set of processes are blocked because each process holds a resource and waits for another resource held by some other process.",
        body_style
    ))

    story.append(Paragraph("5.2 Four Necessary Conditions for Deadlock", h1_style))
    story.append(Paragraph("1. <b>Mutual Exclusion</b>: At least one resource must be held in a non-shareable mode.", bullet_style))
    story.append(Paragraph("2. <b>Hold and Wait</b>: A process must hold at least one resource and wait for additional resources held by others.", bullet_style))
    story.append(Paragraph("3. <b>No Preemption</b>: Resources cannot be preempted; they are released voluntarily only after process completion.", bullet_style))
    story.append(Paragraph("4. <b>Circular Wait</b>: A closed chain of processes exists, such that each process holds resources needed by the next.", bullet_style))

    story.append(Paragraph("5.3 Deadlock Avoidance & Banker's Algorithm", h1_style))
    story.append(Paragraph(
        "The <b>Banker's Algorithm</b> (developed by Edsger Dijkstra) is a deadlock avoidance algorithm. "
        "It tests for safety by simulating resource allocation for maximum declared claims, ensuring the system stays in a <b>Safe State</b> before granting any resource request.",
        body_style
    ))

    doc.build(story)
    print(f"✅ Generated 5-page sample academic PDF at: {PDF_PATH}")

if __name__ == "__main__":
    generate_academic_pdf()
