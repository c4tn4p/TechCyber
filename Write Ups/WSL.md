WSL & tools
===========
Bear with me and quickly spawn a customized WSL instance to do have some cyber fun when you can't access your favorite GNU/Linux pwn station.

We'll use a WSLed version of GNU/Linux Debian 12 (Bookworm) on a Microsoft Windows 11 workstation.

* [WSL & tools](#wsl-&-tools)
   * [In PowerShell](#in-powershell)
   * [In WSL](#in-wsl)
      * [Resolv.conf](#resolvconf)
      * [APT](#apt)
      * [VIM](#vim)

## In PowerShell

Open [Windows Terminal](https://learn.microsoft.com/en-us/windows/terminal/install)

- Updating WSL

```powershell
wsl --update
```

- Make sure you are using [WSL 2](https://learn.microsoft.com/en-us/windows/wsl/install#upgrade-version-from-wsl-1-to-wsl-2)

```powershell
wsl --set-default-version 2
```

- Installing Debian in the latest version available in the Microsoft Store

```powershell
wsl --install -d debian
```

## In WSL

> 🧠 We'll use [heredoc](https://en.wikipedia.org/wiki/Here_document) like crazy here !
> If you want to learn more about it, check this [awesome thread on stackoverflow](https://stackoverflow.com/questions/2500436/how-does-cat-eof-work-in-bash)

- Stay in Windows Terminal and connect to your WSL instance and let's go root for a short time to set things up

```
sudo su -
```

### Resolv.conf

- Editing / creating `/etc/wsl.conf` to tell WSL not to manage the `/etc/resolv.conf` file on its own

```bash
cat << EOF > /etc/wsl.conf
[network]
generateResolvConf = false
EOF
```

- Creating your own `/etc/resolv.conf` to use the[FDN open resolvers](https://www.fdn.fr/actions/dns/)

```bash
cat << EOF > /etc/resolv.conf
# https://www.fdn.fr/actions/dns/
nameserver 80.67.169.12 # ns0.fdn.fr
nameserver 80.67.169.40 # ns1.fdn.fr
EO
```

- Use [chattr](https://fr.wikipedia.org/wiki/Chattr) to add the `i` flag so that WSL won't touch it

```bash
chattr +i /etc/resolv.conf
```

### APT

- Installing `ca-certificates` so we can safely use APT over HTTPS

```bash
apt -y update
apt -y install ca-certificates
```

- Editing the `/etc/apt/sources.list` file to ad an *s* after *http* to use HTTPS instead of plain HTTP

```bash
cat << EOF > /etc/apt/sources.list
deb https://deb.debian.org/debian bookworm main
deb https://deb.debian.org/debian bookworm-updates main
deb https://security.debian.org/debian-security bookworm-security main
deb https://ftp.debian.org/debian bookworm-backports main
EOF
```

- And the download aaaaaaall your favorite tools.

```bash
apt update && apt -y full-upgrade && \
apt -y install \
bzip 2 \
bzip3 \
ccze \
curl \
dnsutils \
git \
haschat \
hping3 \
htop \
iftop \
john \
less \
man \
neofetch \
nethogs \
nmap \
traceroute \
tree \
vim \
wget \
whois
```

### VIM

- Customizing [vim](https://www.vim.org/)'s (aka your favorite text editor) configuration file `/etc/vim/vimrc`

```
cat << EOF > /etc/vim/vimrc
" Source the default Debian Vim configuration
runtime! debian.vim

" Enable syntax highlighting
syntax on

" Ensure compatibility settings are disabled
set nocompatible

" Set a dark background for colorscheme
set background=dark

" Automatically jump to the last position when reopening a file
au BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") | exe "normal! g'\"" | endif

" Enable file type detection and plugin/indent loading
filetype plugin indent on

" Use system clipboard for all operations
set clipboard=unnamedplus

" Ignore case when searching
set ignorecase

" Highlight matches as you type
set incsearch

" Enable mouse support in all modes
set mouse=a

" Show line numbers
set number

" Display incomplete commands
set showcmd

" Highlight matching parenthesis
set showmatch

" Override ignorecase if search pattern contains uppercase letters
set smartcase

" Show cursor position all the time
set ruler

" Split windows below the current one
set splitbelow

" Split windows to the right of the current one
set splitright

" Enable enhanced command-line completion
set wildmenu

" Number of spaces that a <Tab> in the file counts for
set tabstop=4

" Number of spaces to use for each step of (auto)indent
set shiftwidth=4

" Always display the status line
set laststatus=2

" PLUGINS!
" Set the runtime path for plugins
set runtimepath+=~/.vim/pack/plugins/start

" Clone NERDTree plugin if not already installed
if empty(glob('~/.vim/pack/plugins/start/nerdtree'))
  silent !git clone https://github.com/preservim/nerdtree.git ~/.vim/pack/plugins/start/nerdtree
endif

" Clone ALE plugin if not already installed
if empty(glob('~/.vim/pack/plugins/start/ale'))
  silent !git clone https://github.com/dense-analysis/ale.git ~/.vim/pack/plugins/start/ale
endif

" Clone vim-airline plugin if not already installed
if empty(glob('~/.vim/pack/plugins/start/vim-airline'))
  silent !git clone https://github.com/vim-airline/vim-airline ~/.vim/pack/plugins/start/vim-airline
endif

" Clone vim-airline-themes plugin if not already installed
if empty(glob('~/.vim/pack/plugins/start/vim-airline-themes'))
  silent !git clone https://github.com/vim-airline/vim-airline-themes ~/.vim/pack/plugins/start/vim-airline-themes
endif

" Configure NERDTree to open on startup and toggle with Ctrl+n
autocmd vimenter * NERDTree | wincmd p
map <C-n> :NERDTreeToggle<CR>

" Configure ALE for syntax checking
let g:ale_linters = {
\   'python': ['flake8'],
\   'javascript': ['eslint'],
\}

" Configure vim-airline to show tabline and use the 'unique_tail' formatter
let g:airline#extensions#tabline#enabled = 1
let g:airline#extensions#tabline#formatter = 'unique_tail'

" Set the vim-airline theme to 'molokai'
let g:airline_theme='molokai'

" Source a local vimrc file if it exists
if filereadable("/etc/vim/vimrc.local")
  source /etc/vim/vimrc.local
endif
EOF
```
