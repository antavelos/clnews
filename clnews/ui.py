import urwid

navigate_mapper = {
    'up': -1,
    'down': 1
}


def exit_on_q(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()

    if key in ['up', 'down']:
        fc = columns.get_focus_column()
        listbox = channel_listbox if fc == 0 else event_listbox
        listbox_navigate(listbox, key)


def listbox_navigate(listbox, key):
    _, idx = listbox.get_focus()
    idx = (idx + navigate_mapper[key]) % len(listbox.body)
    listbox.set_focus(idx)

palette = [
    ('title', 'black', 'light gray'),
    ('date', 'white', 'dark red'),
    ('channel', 'black', 'light gray', 'standout'),
    ('summary', 'black', 'light gray'),
    ('streak', 'black', 'light gray'),
    ('separator', 'black', 'light gray'),
    ('header', 'white', 'dark blue'),
    ('reveal focus', 'black', 'dark cyan', 'standout')]

event_text = urwid.Text([('title', u" Title - "),
                         ('date', u"1/1/2016\n"),
                         ('summary', u" summary" * 10), '\n'], align='left')
event = urwid.AttrMap(event_text, None, 'reveal focus')


event_list = urwid.SimpleListWalker([event, event, event])
event_listbox = urwid.ListBox(event_list)

event_header_text = urwid.Text("Showing X events", wrap='clip')
event_header = urwid.AttrMap(event_header_text, 'header')
event_column = urwid.Frame(event_listbox, event_header)

channel_text = urwid.Text(u" Channel", align='left')
channel = urwid.AttrMap(channel_text, None, 'reveal focus')

channel_list = urwid.SimpleListWalker([channel, channel, channel])
channel_listbox = urwid.ListBox(channel_list)

channel_header_text = urwid.Text("My channels", wrap='clip')
channel_header = urwid.AttrMap(channel_header_text, 'header')
channel_column = urwid.Frame(channel_listbox, channel_header)

separator = urwid.AttrWrap(urwid.SolidFill(u'\u2502'), 'separator')

columns = urwid.Columns([('weight', 1, channel_column),
                         ('fixed', 1, separator),
                         ('weight', 5, event_column)],
                        dividechars=0, focus_column=0)

linebox = urwid.LineBox(columns)
loop = urwid.MainLoop(linebox, palette, unhandled_input=exit_on_q)
loop.run()
