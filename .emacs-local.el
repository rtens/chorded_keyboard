(add-hook 'emacs-startup-hook
          (lambda ()
            (split-window-horizontally -25)
	    (other-window 1)
	    (if (eq system-type 'windows-nt)
		(progn
		  (eshell)
		  (with-current-buffer "*eshell*"
		    (visual-line-mode)
		    (eshell-return-to-prompt)
		    (insert "venv/Scripts/ptw.exe -- -q")
		    (eshell-send-input)))
	      (term "./venv/bin/ptw -- -q")
	      )
	    (other-window 1)
	    )
	  )

