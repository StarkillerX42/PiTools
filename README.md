# PiTools

A library of scripts to be used with a raspberry pi

### Author

Dylan Gatlin
dgatlin@apo.nmsu.edu

## Fan

A gpio controller for a raspberry pi fan, best daemonized using crontab with the
 command
 ```fan.py 2 60
 ```

## Temperature Logger

This is a simple structure to keep track of my raspbery pi's temperature. I run
 it in crontab hourly, and I invented it because my pi got too hot when running
 StarkillerX42/Alarm/alarm.py.

## GNU License

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

