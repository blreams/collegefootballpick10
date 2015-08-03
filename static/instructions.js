function get_instr() {
    s = "<div class=\"instructions\">Game Final Instructions</div>" +
        "<div id=\"instructions-content\"> 1. fill in the score and check final</div><br>" +
        "<div class=\"instructions\">Game In Progress Instructions</div>" +
        "<div id=\"instructions-content\">" +
            "1. uncheck final<br>" +
            "2. fill in the current score<br>" +
            "3. fill in the quarter (1st, 2nd, Half, 3rd, 4th, OT, 2OT, 3OT,...)<br>" +
            "4. fill in the time left in the quarter if not halftime (minutes:seconds)<div><br>" +
        "<div class=\"instructions\">Game Not Started Instructions</div>" +
        "<div id=\"instructions-content\">" +
            "1. uncheck final<br>" +
            "2. the scores should be blank<div><br><br>";
    return s;
}

function expand_instr() {
    document.getElementById("instr-link").setAttribute("onclick","collapse_instr()");
    document.getElementById("instr-link").innerHTML = "[-]";
    document.getElementById("instr-content").innerHTML = get_instr();
    return false;
}

function collapse_instr() {
    document.getElementById("instr-link").setAttribute("onclick","expand_instr()");
    document.getElementById("instr-link").innerHTML = "[+]";
    document.getElementById("instr-content").innerHTML = "";
    return false;
}
