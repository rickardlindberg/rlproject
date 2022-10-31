I want to try and implement a projectional editor.

Inspiration: https://github.com/projectured/projectured

Plain file ->
Parsed structure ->
Projected as graphics (plus cursor) ->
Keyboard triggers change in parsed structure ->
    Parsed structure is rendered back to plain file
    +
    Parsed structure is projected again

The graphical projection is a tree of boxes. Each box can have different layout
constraints and algorithms. Boxes are cached. Id of immutable parsed
structure.

* Should not manage windows, leave that to window manager

https://research.swtch.com/acme
https://research.swtch.com/acme.pdf

Projectional editor to analyze RLMeta intermediate results. RLMeta IDE.

---

https://github.com/projectured/projectured/wiki:

* Bidirectional, multistage projections between problem domains

* "For example, printing to a graphical display needs a projection from the
  domain being edited to the graphics domain (the domain of the output
  device)."

* "For example, reading from a keyboard needs a projection from the keyboard
  domain (the domain of the input device) to the domain being edited."

* Domain: "It describes the data structures of documents, selections and
  operations that belong to a problem domain."

* Projection: "Simply speaking it's a transformation from one domain to
  another. A projection transforms the domain specific data structures of
  documents, selections and operations."

* Does a backend need a specific projection domain?

    * SDL backend needs WIDGET/COMPOSITE?

---

https://www.projectit.org/010_Intro/010_Projectional_Editing

> The essential characteristic of projectional editing is that the user
> manipulates the Abstract Syntax Tree (AST) directly. In contrast, the
> traditional manner of editing is that a user manipulates a text-string, which
> is then (re)parsed into a (changed) AST.

> 1. The model/AST is mapped to a visual presentation (the projection).
> 2. The projection is shown to the user.
> 3. The user performs an action on the projection.
> 4. The action on the projection is mapped to an action on the model/AST.
> 5. (or 1 again) The changed model/AST is (re)mapped to a visual representation.

https://www.projectit.org/030_Developing_a_Language/030_API_Level/020_Writing_Projections

---

https://github.com/tehwalris/forest

https://www.youtube.com/watch?v=ze_nJlKkckg

* Multiple cursors

---

* You always edit the bottom most document

---

* Where to do convert keystrokes to actions?
* Multiple cursors?
* If editor is modal or not should only be reflected in key bindings

* Operation 1: replace multiple words
    * Move cursor to word
    * `*` to select word to create multiple cursors
    * `c` to enter insert mode and do the replacement
    * `Esc` to exit

* Operation 2: filter lines and operate on those only
    * Enter filter `test`
        * Show only lines matching filters
    * Cursor and edit operations should only work on filtered lines

* Line number projection

* Word wrap projection
