# ~/.bashrc: executed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)
# for examples

# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac

#BCH section at bottom!

# don't put duplicate lines or lines starting with space in the history.
# See bash(1) for more options
HISTCONTROL=ignoreboth

# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=1000
HISTFILESIZE=2000

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# If set, the pattern "**" used in a pathname expansion context will
# match all files and zero or more directories and subdirectories.
#shopt -s globstar

# make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# set variable identifying the chroot you work in (used in the prompt below)
if [ -z "${debian_chroot:-}" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

# set a fancy prompt (non-color, unless we know we "want" color)
case "$TERM" in
    xterm-color) color_prompt=yes;;
esac

# uncomment for a colored prompt, if the terminal has the capability; turned
# off by default to not distract the user: the focus in a terminal window
# should be on the output of commands, not on the prompt
#force_color_prompt=yes

if [ -n "$force_color_prompt" ]; then
    if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
	# We have color support; assume it's compliant with Ecma-48
	# (ISO/IEC-6429). (Lack of such support is extremely rare, and such
	# a case would tend to support setf rather than setaf.)
	color_prompt=yes
    else
	color_prompt=
    fi
fi

if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
else
    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
fi
unset color_prompt force_color_prompt

# If this is an xterm set the title to user@host:dir
case "$TERM" in
xterm*|rxvt*)
    PS1="\[\e]0;${debian_chroot:+($debian_chroot)}\u@\h: \w\a\]$PS1"
    ;;
*)
    ;;
esac

# enable color support of ls and also add handy aliases
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    #alias dir='dir --color=auto'
    #alias vdir='vdir --color=auto'

    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi

# some more ls aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'

# Add an "alert" alias for long running commands.  Use like so:
#   sleep 10; alert
alias alert='notify-send --urgency=low -i "$([ $? = 0 ] && echo terminal || echo error)" "$(history|tail -n1|sed -e '\''s/^\s*[0-9]\+\s*//;s/[;&|]\s*alert$//'\'')"'

# Alias definitions.
# You may want to put all your additions into a separate file like
# ~/.bash_aliases, instead of adding them here directly.
# See /usr/share/doc/bash-doc/examples in the bash-doc package.

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
if ! shopt -oq posix; then
  if [ -f /usr/share/bash-completion/bash_completion ]; then
    . /usr/share/bash-completion/bash_completion
  elif [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
  fi
fi

#bch:
export PS1='\W> '
export POSTGIS_GDAL_ENABLED_DRIVERS=GTiff
export POSTGIS_ENABLE_OUTDB_RASTERS=1
export PATH="${HOME}/.local/bin:$PATH"
export PIPENV_VENV_IN_PROJECT=1

alias skyl='cd /home/bret/servers/repo-skylinesC/skylinesC/'
alias esky='cd /home/bret/servers/repo-skylinesC/skylinesC/ember'
alias eserve5='esky;sudo ember serve --environment=production --port 80 --proxy http://localhost:5000/'
alias eserve42-5='esky;sudo ember serve --environment=production --port 4200 --proxy http://localhost:5000/'

alias mserve='skyl; pipenv run ./manage.py runserver'
alias dbrecreate='pipenv run ./manage.py db recreate'
alias dbcreate='pipenv run ./manage.py db create'
alias pycharm='./pycharm/bin/pycharm.sh'
alias pgadmin='python ~/.local/share/virtualenvs/pgadmin-WsDn56it/lib/python2.7/site-packages/pgadmin4/pgAdmin4.py'
alias pips='source venv/bin/activate'
alias ngstart="sudo systemctl start nginx"
alias ngstop="sudo systemctl stop nginx"
alias ngrestart="sudo systemctl restart nginx"
alias ngstatus="systemctl status nginx"
alias ngreload="sudo kill -HUP `cat /var/run/nginx.pid`"
alias ngvim-default="sudo vim /etc/nginx/sites-available/default"
alias ngvim-skylinesC='sudo vim /etc/nginx/sites-available/skylinescondor.com'
alias ngvim-nginx.conf="sudo vim /etc/nginx/nginx.conf"
alias ngerror.log="sudo tail -f -n200 /var/log/nginx/error.log"
alias ngaccess.log="sudo tail -f -n200 /var/log/nginx/access.log"
alias ngcd="cd /etc/nginx/"
alias ngt="sudo nginx -t"
alias ptest='skyl; python3 production/tests/pageSLCtest.py'
alias group="cd groupFlights;pips;python groupflights.py"

alias photo='ssh root@hessminecraft.cyou'
alias dcu='docker-compose up'
alias dcr='docker rm -f $(docker ps -aq)'
alias dc='docker-compose'
alias dcd='docker-compose down --rmi all'
alias dcp='docker system prune -a -f'
alias grcr='grep CRON /var/log/syslog'
alias ll='ls -l'
alias wc='wc -l'
alias ncdu='/home/bret/ncduDiskUsage/ncdu -x'
alias pfr='sudo service postfix restart'
alias ms='cd /home/bret/mail-server/; pipenv run python mail-server.py'
nginxconfigbackup() { 
  sudo cp /etc/nginx/sites-available/skylinescondor /etc/nginx/sites-available/skylinescondor.$(date "+%Y-%m-%d_%H:%M")-$1
}

#the parameter ending is the comment use dashes "-" between words

#end bch

