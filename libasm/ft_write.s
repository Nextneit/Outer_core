section	.text
global	ft_write
extern	__errno_location

ft_write:
	;call write syscall (rax = 1)
	mov		rax, 1
	syscall

	;check if syscall returned error
	test	rax, rax
	jns		.ok

	;handle error: negate return value
	neg		rax
	mov		edi, eax
	;align stack for function call
	sub		rsp, 8
	call	__errno_location wrt ..plt
	;set errno with error code
	mov		dword[rax], edi
	add		rsp, 8

	;return -1 on error
	mov		rax, -1
	ret

.ok:
	;return number of bytes written
	ret