# start new with session name
tmux new -s myname

# attach
tmux a -t myname

# list sessions
tmux ls

# kill session
tmux kill-session -t myname

# detach
# Ctrl b + d