# ch35t

Ch35t (pronounced “chest”) is, well, a chest with a little
bit of [3564020356](http://3564020356.org) in it :-)

More precisely, it is an open format you can use to describe
riddles or, more generally, different kinds of encrypted 
resources, together with hints on how to decrypt them.

Following the “treasure chest” metaphor, in the ch35t format:

- chests can only be opened with the right key (or set of)
- one can provide, together with a chest, some hints to find its key
- chests may have something hidden inside them, ie they come with
  some content (payload) that you can access only after you open them

All of this is described in a JSON file that can be shared 
however you see fit (if you want, you can even hide it into
another chest!). And you don’t have to worry about making your
chest accessible to everyone, as you can use encryption to hide
a key or lock contents inside a chest.

## Q: Why a format?

Because this way the riddle is completely decoupled from who
created it and where you found it, moving the focus on its
actual content. Here are some other advantages:

- **easy sharing**: you can just provide a link to a JSON file
  for hours of potential fun (or frustration ;-))
- **playing offline**: once you have downloaded a chest its
  contents reside on your computer, so you don’t have to
  worry about being online to unlock it
- **compositionality**: you can build your own “treasure hunt”
  by collecting riddles created by other people and chaining
  them into your own custom game
- **flexibility**: ch35t allows you to provide hints and payloads
  in different formats, lock with different encryption
  algorithms, and react differently to different file types
- **extensibility**: while here you can find examples for handling
  a few data types and encryption methods, everyone can
  implement their own extension or even a new client. You can
  have a TUI or a Web-based one, you can build a custom
  leaderboard, and so on.


## Q: How/where is this format defined?

To define the Ch35t format I decided to rely on [JSON Schema](https://json-schema.org/).
This way you can easily test the validity of your chest file, and
I can easily generate documentation starting from a properly 
commented schema file.

You can find the JSON definition [here](./schema/1.0.0.json), and
a human-readable, markdown version [here](./schema.md).


## Q: Sounds great! How can I play with it?

Ehm... Development is still in an early phase. Very early :-)
But hey, this is at least 50% of the “release early, release often” paradigm!
Also, this does not mean there is nothing to play with yet:


### What is currently available

- a [v1.0.0](./schema/1.0.0.json) of the format [schema](./schema.md)
- a [notebook](./testing_ch35t.ipynb) explaining the basics of Ch35t
  (and showing you how to start playing with very simple examples)
- a few ready-to-play chests in the examples folder, replicating the
  first two riddles on [3564020356](http://3564020356.org/): 
  [Deserve](examples/deserve.json), [Riddle02](examples/riddle02.json)


### Planned features

Here is a list of features that I would like to see in my 
ideal v1.0 of Ch35t:

- [x] an actual format definition (v1.0.0 is a good start, but there
  is definitely space for improvement)
- [ ] an improved notebook that should act as a tutorial, explaining
  the format with more detail and allowing people to play
  with examples (currently WIP)
- [ ] adding signatures, so we can have proper attribution and
  guarantee riddle authenticity
- [ ] improving modularity (I’d like to see chests with many keys
  and give the possibility to open them with different
  combinations of them, e.g. just one, at least N, all in a
  given order, etc.)
- [ ] a simple client with all the basic features (TUI or simple
  containerized web-based implementation, so people can just play
  with it without requiring any installation
- [ ] more handlers (e.g. I would love to use
  [Tomb](https://dyne.org/software/tomb/) for a “russian dolls” 
  kind of riddle)
- [ ] a few more riddles (I would like to convert some from 356s
  so they become accessible to everyone
- [ ] a set of tools to help people build their own chests


### How can I create/share my own chests?

The whole purpose of Ch35t is allowing anyone to build and openly
share their own riddles. To make a riddle, create a JSON file
that is compliant with the Ch35t format and can be parsed by the
Ch35t client (which -yes I know- in this moment boils down to few
lines of code in a notebook...). 
Sharing the riddle is easier: just upload it somewhere and share
its URL on your favorite channels! I have just started posting
Ch35t-related updates on the Fediverse using the 
[#Ch35t](https://fosstodon.org/tags/Ch35t) tag, you are very
welcome to do the same!