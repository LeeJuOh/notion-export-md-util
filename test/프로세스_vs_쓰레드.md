# 프로세스 vs 쓰레드

### **프로세스(Process)**

- 프로세스는 실행 중인 프로그램
- 즉 프로세스는 os의 작업 단위
- 프로세스가 실행되기 위해서는 아래의 자원 필요하며 os로부터 할당받음
    - cpu time
    - memory
    - files
    - I/O devices
- 여러개의 섹션을 가짐
    - text(code) section: 실행 코드
    - data section: 전역 변수
    - heap section: 동적 할당된 메모리
    - stack section: 임시 데이터 저장소 지역 변수, 함수 파라미터, 리턴 address 등
- 5가지의 상태를 가짐
    - new: the process is being created.
    - running: Instructions are being executed
    - waiting : the process is waiting for some event to occur, 입출력 완료 및 수신
    - ready: the process is waiting to be assigned to a processor.
    - terminated: the process has finished execution.

![image_1](./프로세스_vs_쓰레드/1.png)

### **프로세스 제어 블록(Process Control Block, PCB) or TCB**

- PCB 는 특정 **프로세스에 대한 중요한 정보를 저장**
    - 프로세스 식별자(Process ID, PID) : 프로세스 식별번호
    - 프로세스 상태 : new, ready, running, waiting, terminated 등의 상태를 저장
    - 프로그램 카운터 : 프로세스가 다음에 실행할 명령어의 주소
    - CPU 레지스터
    - CPU 스케쥴링 정보 : 프로세스의 우선순위, 스케줄 큐에 대한 포인터 등
    - 메모리 관리 정보 : 페이지 테이블 또는 세그먼트 테이블 등과 같은 정보를 포함
    - 입출력 상태 정보 : 프로세스에 할당된 입출력 장치들과 열린 파일 목록
    - 어카운팅 정보 : 사용된 CPU 시간, 시간제한, 계정번호 등
- 문맥 교환(context switching)이 일어나면 이전 프로세스 정보를 pcb에 저장하고 새 프로세스의 정보를 pcb에서 읽어온다
    - 문맥교환: 프로세스의 상태 정보를 저장하고 복원하는 일련의 과정

### **스레드(Thread)**

- 프로세스 내에서 실행 흐름의 단위
- 스레드 ID, 프로그램 카운터, 레지스터 집합, 그리고 스택으로 구성
- 같은 프로세스에 속한 다른 스레드와 코드, 데이터 섹션, 그리고 열린 파일이나 신호와 같은 운영체제 자원들을 공유
- 

### **스택을 스레드마다 독립적으로 할당하는 이유**

- 스레드의 정의에 따라 독립적인 실행 흐름을 추가하기 위해 최소 조건으로 독립된 스택을 할당한다.
    - 스택은 함수 호출 시 전달되는 인자, 되돌아갈 주소값 및 함수 내에서 선언하는 변수 등을 저장하기 위해 사용되는 메모리 공간이다.
    - 스택 메모리 공간이 독립적이라는 것은 독립적인 함수 호출이 가능하다는 것이고 이는 독립적인 실행 흐름이 가능하게 한다.

### **PC Register 를 스레드마다 독립적으로 할당하는 이유**

- 명령어가 연속적으로 수행되지 못하기 때문에 어느 부분까지 수행했는지 기억하기 위해서 PC 레지스터를 독립적으로 할당한다.
    - PC 값은 스레드가 명령어의 어디까지 수행하였는지를 나타나게 된다
    - 스레드는 CPU 를 할당받았다가 스케줄러에 의해 다시 선점당한다.