package org.pentaho.build.buddy.bundles.api.build.impl;

import org.pentaho.build.buddy.bundles.api.build.BuildCommands;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/**
 * Created by bryan on 3/18/16.
 */
public class BuildCommandsImpl implements BuildCommands {
    private final List<String> commands;
    private final String cleanupCommand;

    public BuildCommandsImpl(String before, String command, String cleanupCommand) {
        this(new ArrayList<>(Arrays.asList(before, command)), cleanupCommand);
    }

    public BuildCommandsImpl(List<String> commands, String cleanupCommand) {
        this.commands = commands;
        this.cleanupCommand = cleanupCommand;
    }

    @Override
    public List<String> getCommands() {
        return commands;
    }

    @Override
    public String getCleanupCommand() {
        return cleanupCommand;
    }
}