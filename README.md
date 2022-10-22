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
