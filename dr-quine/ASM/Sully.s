section .data
	s: db "section .data%1$c%2$cs: db %4$c%5$s%4$c,0%1$c%2$cfmt: db %4$cSully_%%d.s%4$c,0%1$c%2$cmode: db %4$cw%4$c,0%1$c%2$ccmd: db %4$cnasm -f elf64 Sully_%%d.s && gcc -no-pie Sully_%%d.o -o Sully_%%d && ./Sully_%%d%4$c,0%1$c%1$csection .bss%1$c%2$cfilename: resb 32%1$c%2$ccmdbuf: resb 256%1$c%1$csection .text%1$c%2$cglobal main%1$c%2$cextern sprintf%1$c%2$cextern fopen%1$c%2$cextern fprintf%1$c%2$cextern fclose%1$c%2$cextern system%1$c%1$cmain:%1$c%2$cpush rbp%1$c%2$cmov rbp,rsp%1$c%2$cpush r12%1$c%2$cpush r15%1$c%2$csub rsp,32%1$c%2$cmov r15d,%3$d%1$c%2$ccmp r15d,0%1$c%2$cjl .end%1$c%2$clea rdi,[filename]%1$c%2$clea rsi,[fmt]%1$c%2$cmov rdx,r15%1$c%2$cxor rax,rax%1$c%2$ccall sprintf%1$c%2$clea rdi,[filename]%1$c%2$clea rsi,[mode]%1$c%2$ccall fopen%1$c%2$cmov r12,rax%1$c%2$cmov rdi,r12%1$c%2$clea rsi,[s]%1$c%2$cmov rdx,10%1$c%2$cmov rcx,9%1$c%2$cmov r8,r15%1$c%2$cdec r8%1$c%2$cmov r9,34%1$c%2$clea rax,[s]%1$c%2$csub rsp,8%1$c%2$cpush rax%1$c%2$cxor rax,rax%1$c%2$ccall fprintf%1$c%2$cadd rsp,16%1$c%2$cmov rdi,r12%1$c%2$ccall fclose%1$c%2$ccmp r15d,0%1$c%2$cjle .end%1$c%2$clea rdi,[cmdbuf]%1$c%2$clea rsi,[cmd]%1$c%2$cmov rdx,r15%1$c%2$cmov rcx,r15%1$c%2$cmov r8,r15%1$c%2$cmov r9,r15%1$c%2$cxor rax,rax%1$c%2$ccall sprintf%1$c%2$clea rdi,[cmdbuf]%1$c%2$ccall system%1$c.end:%1$c%2$cxor rax,rax%1$c%2$cleave%1$c%2$cret%1$c",0
	fmt: db "Sully_%d.s",0
	mode: db "w",0
	cmd: db "nasm -f elf64 Sully_%d.s && gcc -no-pie Sully_%d.o -o Sully_%d && ./Sully_%d",0

section .bss
	filename: resb 32
	cmdbuf: resb 256

section .text
	global main
	extern sprintf
	extern fopen
	extern fprintf
	extern fclose
	extern system

main:
	push rbp
	mov rbp,rsp
	push r12
	push r15
	sub rsp,32
	mov r15d,5
	cmp r15d,0
	jl .end
	lea rdi,[filename]
	lea rsi,[fmt]
	mov rdx,r15
	xor rax,rax
	call sprintf
	lea rdi,[filename]
	lea rsi,[mode]
	call fopen
	mov r12,rax
	mov rdi,r12
	lea rsi,[s]
	mov rdx,10
	mov rcx,9
	mov r8,r15
	dec r8
	mov r9,34
	lea rax,[s]
	sub rsp,8
	push rax
	xor rax,rax
	call fprintf
	add rsp,16
	mov rdi,r12
	call fclose
	cmp r15d,0
	jle .end
	lea rdi,[cmdbuf]
	lea rsi,[cmd]
	mov rdx,r15
	mov rcx,r15
	mov r8,r15
	mov r9,r15
	xor rax,rax
	call sprintf
	lea rdi,[cmdbuf]
	call system
.end:
	xor rax,rax
	leave
	ret
