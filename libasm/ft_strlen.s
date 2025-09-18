section .text
global ft_strlen

ft_strlen:
	;initialize counter to 0
	xor rax, rax

.compare:
	;check if current byte is null terminator
	cmp BYTE [rdi + rax], 0
	je .done
	;increment counter and continue
	inc rax
	jmp .compare

.done:
	;return length in rax
	ret
	