# **************************************************************************** #
#                                   FT_PING                                    #
# **************************************************************************** #

# Colors
GREEN = \033[0;32m
RED = \033[0;31m
BLUE = \033[0;34m
NC = \033[0m

# Project
NAME        = ft_ping

# Compiler
CC          = gcc
CFLAGS      = -Wall -Wextra -Werror -g3
LDFLAGS     = -lm

# Directories
SRCDIR     = src
OBJDIR     = obj
INCDIR     = include

# Files
SRCS        = main.c parse.c
OBJS        = $(SRCS:%.c=$(OBJDIR)/%.o)

# Includes
INCLUDES     = -I$(INCDIR)

# ============================================================================ #
#                                    REGLAS                                     #
# ============================================================================ #

all: $(NAME)

$(NAME): $(OBJS)
	@$(CC) $(CFLAGS) $(OBJS) $(LDFLAGS) -o $(NAME)
	@echo "$(GREEN)✅ $(NAME) compiled!$(NC)"
	@echo "$(BLUE)⚙️  Setting network capabilities...$(NC)"
	@sudo setcap cap_net_raw+ep $(NAME) 2>/dev/null && \
		echo "$(GREEN)✅ Network capabilities set!$(NC)" || \
		echo "$(RED)⚠️  Could not set capabilities. Run as root.$(NC)"

$(OBJDIR)/%.o: $(SRCDIR)/%.c
	@mkdir -p $(OBJDIR)
	@$(CC) $(CFLAGS) $(INCLUDES) -c $< -o $@
	@echo "$(BLUE)🔨 Compiling $<$(NC)"

clean:
	@rm -rf $(OBJDIR)
	@echo "$(RED)🧹 Cleaned object files!$(NC)"

fclean: clean
	@rm -f $(NAME)
	@echo "$(RED)🗑️  Full clean!$(NC)"

re: fclean all

debug: CFLAGS += -DDEBUG -fsanitize=address -fsanitize=undefined
debug: re
	@echo "$(BLUE)🐛 Debug mode enabled$(NC)"

test: all
	@echo "$(GREEN)🧪 Testing ft_ping...$(NC)"
	@./$(NAME) -?
	@echo "\n$(BLUE)Testing localhost:$(NC)"
	@sudo ./$(NAME) 127.0.0.1 -c 3 || echo "$(RED)Requires root privileges$(NC)"

setup:
	@mkdir -p $(SRCDIR) $(OBJDIR) $(INCDIR)
	@touch $(SRCDIR)/main.c $(SRCDIR)/parse.c $(SRCDIR)/icmp.c
	@touch $(SRCDIR)/network.c $(SRCDIR)/dns.c $(SRCDIR)/statistics.c
	@touch $(SRCDIR)/signals.c $(SRCDIR)/utils.c $(SRCDIR)/checksum.c
	@touch $(INCDIR)/ft_ping.h
	@echo "$(GREEN)📁 Project structure created!$(NC)"

help:
	@echo "$(BLUE)Available targets:$(NC)"
	@echo "  $(GREEN)make$(NC) or $(GREEN)make all$(NC)    - Compile the project"
	@echo "  $(GREEN)make clean$(NC)          - Remove object files"
	@echo "  $(GREEN)make fclean$(NC)         - Remove all generated files"
	@echo "  $(GREEN)make re$(NC)             - Recompile everything"
	@echo "  $(GREEN)make debug$(NC)          - Compile with debug flags"
	@echo "  $(GREEN)make test$(NC)           - Run basic tests"
	@echo "  $(GREEN)make setup$(NC)          - Create project structure"

.PHONY: all clean fclean re debug test setup help
