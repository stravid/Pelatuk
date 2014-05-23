import sublime, sublime_plugin, os, re

def applescript_path():
  return sublime.packages_path() + "/plugin_one/sendCommand.scpt"

def run_applescript(view, command):
  view.window().run_command("exec", {
    "cmd": [
      "osascript",
      applescript_path(),
      "plugin_one",
      command
    ]
  })

class BaseTestCommand:
  def file_name(self):
    return os.path.basename(self.view.file_name())

  def directory_of_file(self):
    return os.path.dirname(self.view.file_name())

class RunCursorPositionCommand(sublime_plugin.TextCommand, BaseTestCommand):
  def run(self, edit):
    pattern = re.compile("test '(.*)' do")
    region = self.view.sel()[0]
    line = self.view.full_line(region)
    line_content = self.view.substr(line)

    lines_above = reversed(self.view.lines(sublime.Region(0, line.b)))

    for line_above in lines_above:
      line_above_content = self.view.substr(line_above)

      if re.search(pattern, line_above_content):
        test_name = re.search(pattern, line_above_content).groups()[0]
        command = "clear; cd " + self.directory_of_file() + "; bundle exec rake test TEST=" + self.view.file_name() + " TESTOPTS=\"--name=test_" + test_name.replace(' ', '_') + "\""
        run_applescript(self.view, command)

        break

class RunCurrentFileCommand(sublime_plugin.TextCommand, BaseTestCommand):
  def run(self, edit):
    if "_test.rb" in self.file_name():
      command = "clear; cd " + self.directory_of_file() + "; bundle exec rake test TEST=" + self.view.file_name()
      run_applescript(self.view, command)

class RunEverythingCommand(sublime_plugin.TextCommand, BaseTestCommand):
  def run(self, edit):
    command = "clear; cd " + self.directory_of_file() + "; bundle exec rake test"
    run_applescript(self.view, command)
