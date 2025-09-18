NAME = libft.a
FLAGS = -Wall -Werror -Wextra
FILES = ./ft_is/ft_isalnum.c\
		./ft_is/ft_isalpha.c\
		./ft_is/ft_isascii.c\
		./ft_is/ft_isdigit.c\
		./ft_is/ft_isprint.c\
		./str_utils/ft_strlen.c\
		./str_utils/ft_strncmp.c\
		./utils/ft_tolower.c\
		./utils/ft_toupper.c\
		./memory/ft_memset.c\
		./utils/ft_bzero.c\
		./memory/ft_memmove.c\
		./memory/ft_memcpy.c\
		./str_utils/ft_strlcpy.c\
		./str_utils/ft_strlcat.c\
		./str_utils/ft_strchr.c\
		./str_utils/ft_strrchr.c\
		./memory/ft_memcmp.c\
		./memory/ft_memchr.c\
		./str_utils/ft_strnstr.c\
		./utils/ft_atoi.c\
		./memory/ft_calloc.c\
		./str_utils/ft_strdup.c\
		./str_utils/ft_substr.c\
		./str_utils/ft_strjoin.c\
		./str_utils/ft_strtrim.c\
		./utils/ft_itoa.c\
		./str_utils/ft_strmapi.c\
		./str_utils/ft_striteri.c\
		./fd_write/ft_putchar_fd.c\
		./fd_write/ft_putstr_fd.c\
		./fd_write/ft_putendl_fd.c\
		./fd_write/ft_putnbr_fd.c\
		./str_utils/ft_split.c\
		./list/ft_lstnew_bonus.c\
		./list/ft_lstadd_front_bonus.c\
		./list/ft_lstsize_bonus.c\
		./list/ft_lstlast_bonus.c\
		./list/ft_lstadd_back_bonus.c\
		./list/ft_lstdelone_bonus.c\
		./list/ft_lstclear_bonus.c\
		./list/ft_lstiter_bonus.c\
		./list/ft_lstmap_bonus.c\
		./ft_printf/ft_printchar.c\
		./ft_printf/ft_printptr.c\
		./ft_printf/ft_printnbr.c\
		./ft_printf/ft_printf.c\
		./get_next_line/get_next_line_bonus.c\
		./get_next_line/get_next_line_utils_bonus.c

OBJDIR = obj
OBJS = $(addprefix $(OBJDIR)/, $(notdir $(FILES:.c=.o)))

all : $(NAME)

$(OBJDIR):
	mkdir -p $(OBJDIR)

$(NAME) : $(OBJDIR) $(OBJS)
	ar rcs $(NAME) $(OBJS)

$(OBJDIR)/%.o: ./ft_is/%.c
	gcc $(FLAGS) -c $< -o $@

$(OBJDIR)/%.o: ./str_utils/%.c
	gcc $(FLAGS) -c $< -o $@

$(OBJDIR)/%.o: ./utils/%.c
	gcc $(FLAGS) -c $< -o $@

$(OBJDIR)/%.o: ./memory/%.c
	gcc $(FLAGS) -c $< -o $@

$(OBJDIR)/%.o: ./fd_write/%.c
	gcc $(FLAGS) -c $< -o $@

$(OBJDIR)/%.o: ./list/%.c
	gcc $(FLAGS) -c $< -o $@

$(OBJDIR)/%.o: ./ft_printf/%.c
	gcc $(FLAGS) -c $< -o $@

$(OBJDIR)/%.o: ./get_next_line/%.c
	gcc $(FLAGS) -c $< -o $@

clean:
	rm -f $(OBJS)

fclean:
	rm -f $(NAME) $(OBJS)
	rm -rf $(OBJDIR)

re: fclean all

bonus: $(OBJDIR) $(OBJS)
	ar rcs $(NAME) $(OBJS)

.PHONY : all re fclean clean