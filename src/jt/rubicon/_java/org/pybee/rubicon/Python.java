// Copyright (c) 2016-2019, Adam Karpierz
// Licensed under the BSD license
// http://opensource.org/licenses/BSD-3-Clause

package org.pybee.rubicon;

public class Python
{
    // Start the Python runtime.
    //
    // @param pythonHome The value for the PYTHONHOME environment variable
    // @param pythonPath The value for the PYTHONPATH environment variable
    // @param rubiconLib The path to the Rubicon integration library. This library
    //                   will be explictly loaded as part of the startup of the
    //                   Python integration library. If null, it is assumed that
    //                   the system LD_LIBRARY_PATH (or equivalent) will contain
    //                   the Rubicon library
    // @return 0 on success; non-zero on failure.
    //
    public static native int start(String pythonHome, String pythonPath, String rubiconLib);

    // Run the Python script.
    //
    // @param script The path to the Python script to run
    // @return 0 on success; non-zero on failure.
    //
    public static native int run(String script);

    // Stop the Python runtime.
    //
    public static native void stop();

    static
    {
        //!!!System.loadLibrary("rubicon");
    }
}
