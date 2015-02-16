# Thrive-Prototypes

This repo holds various self-contained prototypes and tests of potential Thrive features.

Each prototype gets its own subfolder on the root directory, and can do almost anything it wants within.

Work on a prototype can be committed straight to master, however:
* No commit should affect more than one prototype without a good reason
* It would be good form to use a branch for a specific prototype if master ever starts getting very busy with lots of prototypes being worked on.
* If a prototype gets big and complicated it might be a good idea to do code review through pull requests.
* Commit messages should be descriptive. If you're doing a bugfix on a particular commit for a particular prototype, don't be afraid to use interactive rebase to merge the right commits. Yes, even on master -- prototypes shouldn't depend on each other, so rebasing the commits on one won't bother the others. Remember, rebase responsibly.

Each prototype is responsible for its own documentation -- keep in mind, though, that prototypes are meant to be tweaked and studied. Writing a monolithic spec is a bad idea, but taking extensive notes on ideas, analyses, etc is very good.

I'm not sure what we should use the issue tracker for. Discussion, most likely -- as long as we keep the discussion pertinent to the implementation of prototypes (Comments like "Upboat" and issues like "I have this idea that's really cool but I'm not a programmer so can someone do all the work for me pretty please?" are just asking to be deleted). We could use labels to organize issues by topic (eg, a "membrane" label, a "terrain" label, each with possibly multiple, overlapping prototypes and discussions).

## Why Prototype?
Prototypes are important for testing out aspects of the game before they enter production. You likely knew that already, but this gives us an important way to judge them -- We should learn something from them. Document the reasons behind major decisions, whether the reasons are important technical ones, or teh guiding philosophy behind the prototype. Once a prototype has reached the end of its useful life, it's important to gather all our results together, so we know what the prototype is telling us. If in summing up we uncover more questions, those are often perfect material for new prototypes!
