 Process of editing consists of three steps.



1) Create HTML file with all unique colors:

   Run `./ft.py  ~/.config/flow/themes/<theme-name>.json --make-html`
   
   This step will produce the HTML file `~/.config/flow/themes/<theme-name>.json.html`,
   containing a simple grid with colors: now and new.

 

2) Open it in browser:
   `file:///home/<your-user>/.config/flow/themes/<theme-name>.json.html`.
   Change the color by clicking on the `new` color (native input
   color picker) or directly by editing hex-code (this value is not validating).

   After modifications simply save the page with the same name, to the same location,
   overwriting previous file (without changes).



3) Update the customizable theme using values from 

   `~/.config/flow/themes/<theme-name>.json.html` of first step.

   Run `./ft.py  ~/.config/flow/themes/<theme-name>.json --update-theme`
