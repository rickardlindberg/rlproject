I am building a projectional editor!

I am doing it both to explore the architecture of a projectional editor and
also to see if a projectional editor could be useful for me in some contexts.

## What is a projectional editor?

A projectional editor differs from a text editor in that it can project the
data structure being edited in multiple ways. It is not limited to syntax
highlighted lines of text for example.

It can provide custom projections for different scenarios and provide custom
editing operations for different data structures.

## Videos/Blog posts

### 2022-10-28

[Demo of new project that explores projectional, structured editing.](https://youtu.be/GUX3DQjVg4c)

[![Demo of new project that explores projectional, structured editing.](https://img.youtube.com/vi/GUX3DQjVg4c/maxresdefault.jpg)](https://youtu.be/GUX3DQjVg4c "Demo of new project that explores projectional, structured editing.")

### 2022-11-18

[My projectional editor can do this now?!](https://youtu.be/qa_2Bk4bLyw)

[![My projectional editor can do this now?!](https://img.youtube.com/vi/qa_2Bk4bLyw/maxresdefault.jpg)](https://youtu.be/qa_2Bk4bLyw "My projectional editor can do this now?!")

### 2022-12-15

[How should I evolve the design of my projectional editor?](http://rickardlindberg.me/writing/evolving-design-of-projectional-editor/)

### 2022-02-26

I work on the split algorithm using TDD to help me.

[How TDD helps me solve programming problems.](https://youtu.be/_uB1KGPjJjw)

[![How TDD helps me solve programming problems.](https://img.youtube.com/vi/_uB1KGPjJjw/maxresdefault.jpg)](https://youtu.be/_uB1KGPjJjw "How TDD helps me solve programming problems.")

## Inspiration

My first inspiration for this projects is
[ProjecturEd](https://github.com/projectured/projectured).

Basically I want to build my own version of ProjecturEd. It is written in some
version of Lisp, and I found the codebase difficult to read. It's
documentation however gives a good enough view of the architecture, that I can
try to implement something like that.

## Research

### ProjecturEd

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

### ProjectIt

https://www.projectit.org/010_Intro/010_Projectional_Editing:

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

### Forest

https://github.com/tehwalris/forest

https://www.youtube.com/watch?v=ze_nJlKkckg

I got the idea for multiple cursors from Forest.

After watching the Forste demo, I remembered that Sublime Text (which I have
never used) had multiple cursors as well. I learned a bit about it through
[Exploring The Power Of Multiple Cursors And Selections In Sublime Text
3](https://www.bennadel.com/blog/3798-exploring-the-power-of-multiple-cursors-and-selections-in-sublime-text-3.htm).

### Acme

I watched a demo of Acme and thought it was an interesting editor.

Perhaps some of its ideas are applicable to a projectional editor?

https://research.swtch.com/acme
https://research.swtch.com/acme.pdf

### Tree-sitter

https://tree-sitter.github.io/tree-sitter/

> Tree-sitter is a parser generator tool and an incremental parsing library. It
> can build a concrete syntax tree for a source file and efficiently update the
> syntax tree as the source file is edited.

Can be used for syntax highlighting and language aware contexts/structures?

## Notes

* Should not manage windows, leave that to window manager?

* You always edit the bottom most document

* If editor is modal or not should only be reflected in key bindings

* The graphical projection is a tree of boxes. Each box can have different
  layout constraints and algorithms. Boxes are cached. Id of immutable parsed
  structure.

* Will a rope data structure be useful for better caching/performance?

    * [TCR test && commit || revert -- Rope in Python 1/3](https://youtu.be/Aof0F9DvTFg)

## Use cases

* Editing structured file
    * Plain file ->
    * Parsed structure ->
    * Projected as graphics (plus cursor) ->
    * Keyboard triggers change in parsed structure ->
        * Parsed structure is rendered back to plain file
        * Parsed structure is projected again

* Operation 1: replace multiple words
    * Move cursor to word
    * `*` to select word to create multiple cursors
    * `c` to enter insert mode and do the replacement
    * `Esc` to exit

* Operation 2: filter lines and operate on those only
    * Enter filter `test`
        * Show only lines matching filters
    * Cursor and edit operations should only work on filtered lines

* Operation 3: search and replace across files
    * Enter search term to create a tree result looking like this:
        ./foo.py
            this foo is cool
        ./foo/sub.py
            a sub foo is also cool
    * Select 'foo'
    * Type 'b', 'a', 'r'

* Word wrap projection

* Projectional editor to analyze RLMeta intermediate results. RLMeta IDE.
