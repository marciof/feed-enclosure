# Setup

## Plugin

Either copy, or symlink the provided plugin into the plugins folder:

```
ln -v -s "`realpath -e ext_cmd`" "`./path_to.sh plugins`"
```

## Liferea

Set the environment variable specified in the [`*.plugin` file](./ext_cmd/ext_cmd.plugin):

1. Create a file [setting the variable in `~/.config/environment.d/*.conf`](https://www.freedesktop.org/software/systemd/man/latest/environment.d.html).
2. Logout and login.

### Note

If `DBusActivatable=true` is set in Liferea's `*.desktop` file, then [environment variables defined there won't be passed along](https://developer.gnome.org/documentation/guidelines/maintainer/integrating.html#d-bus-activation).
