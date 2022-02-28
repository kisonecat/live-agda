

(process-send-string "live-emacs" "ls\n")

( list-processes)

(process-send-region "live-emacs" (point-min) (point-max))

(progn
(kill-process "live-emacs")
(start-process "live-emacs" "live-emacs" "python" "/home/jim/live-agda/server.py")
(remove-hook 'post-command-hook 'post-command-hook-fn)
)



(defun post-command-hook-fn ()
  (process-send-string "live-emacs" "%%%point ")  
  (process-send-string "live-emacs" (number-to-string (point)))
  (process-send-string "live-emacs" " ")
  (process-send-string "live-emacs" "mark ")  
  (process-send-string "live-emacs" (number-to-string (mark)))
  (process-send-string "live-emacs" "\n")
  (process-send-string "live-emacs" "%%%buffer%%%\n")
  (process-send-region "live-emacs" (point-min) (point-max))
  (process-send-string "live-emacs" "\n")
  (process-send-string "live-emacs" "%%%EOF%%%\n")
  )

(remove-hook 'post-command-hook 'post-command-hook-fn)


(add-hook 'post-command-hook 'post-command-hook-fn nil :local)

hello there!df

f
sdfdsf

sdfdsf
(post-command-hook-fn)

ffddf


sdfsdf
