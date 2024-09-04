(add-hook 'emacs-startup-hook
          (lambda ()
            (split-window-horizontally -25)
	    (other-window 1)
            (term "./venv/bin/ptw -- -q")
	    (other-window 1)
	    )
	  )

