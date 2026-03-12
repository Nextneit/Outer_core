section .text
global ft_strcmp

ft_strcmp:
	;initialize counters
	xor rcx, rcx
	xor rdx, rdx
	;check if first string is NULL
	cmp rdi, 0
	jz .check_str
	;check if second string is NULL
	cmp rsi, 0
	jz .check_str
	jmp .check

.check_str:
	;compare NULL pointers
	cmp rdi, rsi
	jz .same
	jg .bigger
	jmp .smaller

.compare:
	;load byte from second string and compare
	mov dl, BYTE[rsi + rcx]
	cmp BYTE[rdi + rcx], dl
	jne .compare_last

.increment:
	;move to next character
	inc rcx

.check:
	;check if end of first string
	cmp BYTE [rdi + rcx], 0
	je .compare_last
	;check if end of second string
	cmp BYTE [rsi + rcx], 0
	je .compare_last
	jmp .compare

.compare_last:
	;final comparison: return unsigned byte difference (matches libc strcmp)
	movzx	eax, BYTE [rdi + rcx]
	movzx	edx, BYTE [rsi + rcx]
	sub		eax, edx
	ret

.bigger:
	;return 1 if str1 > str2
	mov rax, 1
	ret

.same:
	;return 0 if strings are equal
	mov rax, 0
	ret

.smaller:
	;return -1 if str1 < str2
	mov rax, -1
	ret
	