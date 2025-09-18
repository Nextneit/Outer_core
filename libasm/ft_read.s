global ft_read
extern __errno_location

ft_read:
	;call read syscall (rax = 0)
	mov rax, 0
	syscall

	;check if syscall returned error
    test    rax, rax
    jns     .ok

	;handle error: save error code and set errno
    mov r8, rax
    call __errno_location wrt ..plt
    mov [rax], r8
    ;return -1 on error
    mov rax, -1
	ret

.ok:
	;return number of bytes read
	ret