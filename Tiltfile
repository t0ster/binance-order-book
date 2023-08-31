docker_compose("compose.yaml")

config.define_string_list("to-run", args=True)
config.define_string_list("to-edit")
cfg = config.parse()

# services to run
config.set_enabled_resources(cfg.get("to-run", ["mongodb"]))

# images to build
to_edit = cfg.get("to-edit", [])
# you can override those in tilt_config.json
