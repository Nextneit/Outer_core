; Outer comment
section .data
	; Inner comment
	s: db "; Outer comment%1$csection .data%1$c%2$c; Inner comment%1$c%2$cs: db %3$c%4$s%3$c,0%1$c%1$csection .text%1$c%2$cglobal main%1$c%2$cextern printf%1$c%1$cmain:%1$c%2$cpush rbp%1$c%2$cmov rbp,rsp%1$c%2$clea rdi,[s]%1$c%2$cmov rsi,10%1$c%2$cmov rdx,9%1$c%2$cmov rcx,34%1$c%2$clea r8,[s]%1$c%2$cxor rax,rax%1$c%2$ccall printf%1$c%2$cxor rax,rax%1$c%2$cpop rbp%1$c%2$cret%1$c",0

section .text
	global main
	extern printf

main:
	push rbp
	mov rbp,rsp
	lea rdi,[s]
	mov rsi,10
	mov rdx,9
	mov rcx,34
	lea r8,[s]
	xor rax,rax
	call printf
	xor rax,rax
	pop rbp
	ret
