# Colors
GREEN = \033[0;32m
RED = \033[0;31m
NC = \033[0m

# Project
NAME = woody_woodpacker

# Compiler
CC = gcc
CFLAGS = -Wall -Wextra -Werror -g
NASM = nasm
NASMFLAGS = -f elf64

# Directories
SRCDIR = src
OBJDIR = obj
LIBFTDIR = libft

# Files
SRCS = main.c utils.c stub.c elf_parser.c crypto.c
OBJS = $(SRCS:%.c=$(OBJDIR)/%.o)

# Libraries
LIBFT = $(LIBFTDIR)/libft.a
INCLUDES = -I$(LIBFTDIR)/includes

# Main targets
all: $(NAME)

$(NAME): $(OBJS) $(LIBFT)
	@$(CC) $(CFLAGS) $(OBJS) -L$(LIBFTDIR) -lft -o $(NAME)
	@echo "$(GREEN)✅ $(NAME) compiled!$(NC)"

$(OBJDIR)/%.o: $(SRCDIR)/%.c
	@mkdir -p $(OBJDIR)
	@$(CC) $(CFLAGS) $(INCLUDES) -c $< -o $@

$(LIBFT):
	@make -C $(LIBFTDIR) --silent

clean:
	@rm -rf $(OBJDIR)
	@make -C $(LIBFTDIR) clean --silent
	@echo "$(RED)🧹 Cleaned!$(NC)"

fclean: clean
	@rm -f $(NAME)
	@make -C $(LIBFTDIR) fclean --silent
	@echo "$(RED)🗑️ Full clean!$(NC)"

re: fclean all

test: all
	@echo "$(GREEN)🧪 Testing...$(NC)"
	@echo '#include <stdio.h>\nint main(){printf("Hello!\\n");return 0;}' > test.c
	@gcc -o test test.c
	@./$(NAME) test
	@./woody
	@rm -f test test.c

setup:
	@mkdir -p $(SRCDIR) $(OBJDIR)
	@touch $(SRCDIR)/woody.c $(SRCDIR)/elf_parser.c $(SRCDIR)/crypto.c
	@echo "$(GREEN)📁 Project structure created!$(NC)"

.PHONY: all clean fclean re test setup