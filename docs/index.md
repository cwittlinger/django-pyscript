# Home

blockdiag {
    file [label="python-script.py"];
    field [label="PyScriptField"];
    params [label="ParameterJSONField"];

    file -> field [];
    field -> params [folded];
}