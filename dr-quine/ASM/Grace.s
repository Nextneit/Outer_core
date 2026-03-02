; Comment
section .data
	s: db "; Comment%1$csection .data%1$c%2$cs: db %3$c%4$s%3$c,0%1$c%2$cf: db %3$cGrace_kid.s%3$c,0%1$c%2$cmode: db %3$cw%3$c,0%1$c%1$csection .text%1$c%2$cglobal main%1$c%2$cextern fopen%1$c%2$cextern fprintf%1$c%2$cextern fclose%1$c%1$cmain:%1$c%2$cpush rbp%1$c%2$cmov rbp,rsp%1$c%2$clea rdi,[f]%1$c%2$clea rsi,[mode]%1$c%2$ccall fopen%1$c%2$cmov r12,rax%1$c%2$cmov rdi,r12%1$c%2$clea rsi,[s]%1$c%2$cmov rdx,10%1$c%2$cmov rcx,9%1$c%2$cmov r8,34%1$c%2$clea r9,[s]%1$c%2$cxor rax,rax%1$c%2$ccall fprintf%1$c%2$cmov rdi,r12%1$c%2$ccall fclose%1$c%2$cxor rax,rax%1$c%2$cpop rbp%1$c%2$cret%1$c",0
	f: db "Grace_kid.s",0
	mode: db "w",0

section .text
	global main
	extern fopen
	extern fprintf
	extern fclose

main:
	push rbp
	mov rbp,rsp
	lea rdi,[f]
	lea rsi,[mode]
	call fopen
	mov r12,rax
	mov rdi,r12
	lea rsi,[s]
	mov rdx,10
	mov rcx,9
	mov r8,34
	lea r9,[s]
	xor rax,rax
	call fprintf
	mov rdi,r12
	call fclose
	xor rax,rax
	pop rbp
	ret
