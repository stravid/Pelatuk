import sublime, sublime_plugin, os, re

call_counter = 0

def applescript_path():
  return sublime.packages_path() + "/plugin_one/sendCommand.scpt"

class RunCursorPositionCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    global call_counter
    call_counter += 1

    print call_counter
    print "RunCursorPositionCommand"

    file_name = os.path.basename(self.view.file_name())
    directory_of_file = os.path.dirname(self.view.file_name())

    pattern = re.compile("test '(.*)' do")
    region = self.view.sel()[0]
    line = self.view.full_line(region)
    line_content = self.view.substr(line)


    lines_above = reversed(self.view.lines(sublime.Region(0, line.b)))

    # print line
    # print lines_above

    for line_above in lines_above:
      line_above_content = self.view.substr(line_above)

      # print line_above_content

      if re.search(pattern, line_above_content):
        test_name = re.search(pattern, line_above_content).groups()[0]

        # print test_name

        self.view.window().run_command("exec", {
          "cmd": [
            "osascript",
            applescript_path(),
            "run_cursor_position",
            "clear; cd " + directory_of_file + "; bundle exec rake test TEST=" + self.view.file_name() + " TESTOPTS=\"--name=test_" + test_name.replace(' ', '_') + "\""
          ]
        })

        break
    #   print line_above

    # if re.search(pattern, line_content) and False:
    #   test_name = re.search(pattern, line_content).groups()[0]
    #   print 'YEAH'
    #   print test_name

    #   self.view.window().run_command("exec", {
    #     "cmd": [
    #       "osascript",
    #       applescript_path(),
    #       "run_cursor_position",
    #       "clear; cd " + directory_of_file + "; bundle exec rake test TEST=" + self.view.file_name() + " TESTOPTS=\"--name=test_" + test_name.replace(' ', '_') + "\""
    #     ]
    #   })

class RunCurrentFileCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    file_name = os.path.basename(self.view.file_name())
    directory_of_file = os.path.dirname(self.view.file_name())

    if "_test.rb" in file_name:
      self.view.window().run_command("exec", {
        "cmd": [
          "osascript",
          applescript_path(),
          "run_cursor_position",
          "clear; cd " + directory_of_file + "; bundle exec rake test TEST=" + self.view.file_name()
        ]
      })

class RunEverythingCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    directory_of_file = os.path.dirname(self.view.file_name())

    self.view.window().run_command("exec", {
      "cmd": [
        "osascript",
        applescript_path(),
        "run_cursor_position",
        "clear; cd " + directory_of_file + "; bundle exec rake test"
      ]
    })
