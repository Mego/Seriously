if (!String.prototype.repeat) {
  String.prototype.repeat = function(count) {
    'use strict';
    if (this == null) {
      throw new TypeError('can\'t convert ' + this + ' to object');
    }
    var str = '' + this;
    count = +count;
    if (count != count) {
      count = 0;
    }
    if (count < 0) {
      throw new RangeError('repeat count must be non-negative');
    }
    if (count == Infinity) {
      throw new RangeError('repeat count must be less than infinity');
    }
    count = Math.floor(count);
    if (str.length == 0 || count == 0) {
      return '';
    }
    // Ensuring count is a 31-bit integer allows us to heavily optimize the
    // main part. But anyway, most current (August 2014) browsers can't handle
    // strings 1 << 28 chars or longer, so:
    if (str.length * count >= 1 << 28) {
      throw new RangeError('repeat count must not overflow maximum string size');
    }
    var rpt = '';
    for (;;) {
      if ((count & 1) == 1) {
        rpt += str;
      }
      count >>>= 1;
      if (count == 0) {
        break;
      }
      str += str;
    }
    return rpt;
  }
}

function toHex(d) {
    return  ("0"+(Number(d).toString(16))).slice(-2).toUpperCase()
}

var cp437 = {};

cp437.codepage = "\u0000\u0001\u0002\u0003\u0004\u0005\u0006\u0007\b\t\n\u000b\f\r\u000e\u000f\u0010\u0011\u0012\u0013\u0014\u0015\u0016\u0017\u0018\u0019\u001a\u001b\u001c\u001d\u001e\u001f !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~ÇüéâäàåçêëèïîìÄÅÉæÆôöòûùÿÖÜ¢£¥₧ƒáíóúñÑªº¿⌐¬½¼¡«»░▒▓│┤╡╢╖╕╣║╗╝╜╛┐└┴┬├─┼╞╟╚╔╩╦╠═╬╧╨╤╥╙╘╒╓╫╪┘┌█▄▌▐▀αßΓπΣσµτΦΘΩδ∞φε∩≡±≥≤⌠⌡÷≈°∙·√ⁿ²■ "

cp437.encode = function(codePoint) {
    return cp437.codepage.charAt(codePoint);
}

cp437.decode = function(c) {
    return cp437.codepage.indexOf(c);
}

function genChar() {
    var code = prompt("Generate CP437 Character:");
    if(!code)
        return;
    $('#code').val($('#code').val() + cp437.encode(parseInt(code)));
    updateUtils();
};

function getByteCount(s) {
    var count = 0, stringLength = s.length;
    s = String(s || "");
    for (var i = 0; i < stringLength; i++) {
        var partCount = encodeURI(s[i]).split("%").length;
        count += partCount == 1 ? 1 : partCount - 1;
    }
    return count;
}

function updateByteCount() {
    var c = $('#code').val();
    var byteCount = c.length;
    var charCount = c.length;
    var s = byteCount + " bytes and " + charCount + " chars long.";
    $('#byteCount').html(s);
}

function getExplanation(code, indent) {
    var string = false;
    var codeBlock = false;
    var listBlock = false;
    var numBlock = false;
    var evalBlock = false;
    var setexp = code == null;
    if(code == null) {
        code = $("#code").val();
    }
    var ind = (indent==null)?'':'\t';
    var explain = '';
    for(var x=0; x < code.length; x++) {
        var c = code.charAt(x);
        if(c === '"') {
            if(string) {
                var prev = code.lastIndexOf('"',x-1);
                var strval = code.slice(prev+1,x);
                explain += ind + 'push the string value "'+strval+'"\r\n'
            }
            string = !string;
            continue;
        } else if(c === '`') {
            if(codeBlock) {
                var prev = code.lastIndexOf('`',x-1);
                var strval = code.slice(prev+1,x);
                explain += ind + 'push the function value `'+strval+'`:\r\n'
                explain += ind + getExplanation(strval,true);
            }
            codeBlock = !codeBlock;
            continue;
        } else if(c === '[') {
            listBlock = true;
            continue;
        } else if(c === ':') {
            if(numBlock) {
                var prev = code.lastIndexOf(':',x-1);
                var strval = code.slice(prev+1,x);
                explain += ind + 'push the numeric value :'+strval+':\r\n'
            }
            numBlock = !numBlock;
            continue;
        } else if(c === cp437.encode(0xEC)) {
            if(evalBlock) {
                var prev = code.lastIndexOf(':',x-1);
                var strval = code.slice(prev+1,x);
                explain += ind + "push the result of eval'ing \""+strval+'"\r\n'
            }
            evalBlock = !evalBlock;
            continue;
        } else if(c === ']') {
            listBlock = false;
            var prev = code.lastIndexOf('[',x-1);
            var strval = code.slice(prev+1,x);
            explain += ind + 'push the list value ['+strval+']\r\n'
            continue;
        }
        if(codeBlock || string || listBlock || numBlock || evalBlock) {
            continue;
        }
        if(c == "'") {
            x++;
            explain += ind + "'" + code.charAt(x) + ": " + 'push the string "' + code.charAt(x) +'"'
        }
        else if(cp437.decode(c) > -1)
            explain += ind + c + ': ' + explanations[toHex(cp437.decode(c))] +'\r\n';
    }
    if(string) {
        var prev = code.lastIndexOf('"',x-1);
        var strval = code.slice(prev+1,x);
        explain += ind + 'push the string value "'+strval+'"\r\n'
    } else if(codeBlock) {
        var prev = code.lastIndexOf('"',x-1);
        var strval = code.slice(prev+1,x);
        explain += ind + 'push the function value `'+strval+'`:\r\n'
        explain += ind + getExplanation(strval,true);
    } else if(listBlock) {
        var prev = code.lastIndexOf('[',x-1);
        var strval = code.slice(prev+1,x);
        explain += ind + 'push the list value "'+strval+'"\r\n'
    } else if(numBlock) {
        var prev = code.lastIndexOf(':',x-1);
        var strval = code.slice(prev+1,x);
        explain += ind + 'push the numeric value "'+strval+'"\r\n'
    } else if(evalBlock) {
        var prev = code.lastIndexOf(cp437.encode(0xEC),x-1);
        var strval = code.slice(prev+1,x);
        explain += ind + 'push the result of eval\'ing "'+strval+'"\r\n'
    }
    if(setexp)
        $('#explanation').html(escapeHTML(explain));
    else
        return explain;
}

function updateHexDump() {
    var hex = '';
    var code = $('#code').val();
    for(var i = 0; i < code.length; i++) {
        var hexi = cp437.decode(code.charAt(i)).toString(16);
        if(hexi.length < 2) hexi = "0" + hexi;
        hex+=hexi;
    }
    $('#hexdump').val(hex);
}

function updateUtils() {
    updateByteCount();
    getExplanation(null);
    updateHexDump();
}

function updateUtilsHex() {
    if(updateCode())
        updateUtils();
}

function updateCode() {
    $("#hexwarn").html();
    var hex = $('#hexdump').val();
    if(hex.length % 2 != 0) {
        return false;
    }
    var code = '';
    for(var i = 0; i < hex.length; i += 2) {
        var val = parseInt(hex.substr(i,2),16);
        if(isNaN(val)) {
            $("#hexwarn").html("error: '"+hex.substr(i,2)+"' is not a valid hex byte (must be in 00-FF)")
            return false;
        }
        code += cp437.encode(val);
    }
    $("#code").val(code);
    return true;
}

function utf8_to_b64(str) {
    return window.btoa(unescape(encodeURIComponent(str)));
}

function b64_to_utf8(str) {
    return decodeURIComponent(escape(window.atob(str)));
}

function escapeHTML(s) {
    var pre = document.createElement('pre');
    var text = document.createTextNode(s);
    pre.appendChild(text);
    return pre.innerHTML;
}

updateUtils();

$(document).ready(
        function() {
            $("#permalink").click(
                    function() {
                        var code = encodeURIComponent(utf8_to_b64(window.JSON.stringify({
                            code : $('#code').val(),
                            input : $('#input').val()
                        })));
                        prompt("Permalink:", "http://"
                                + window.location.hostname + "/link/" + code);
                        window.location.pathname = "/link/" + code;
                    });
            $('#code').on('input propertychange paste', function() {
                updateUtils();
            });
            $('#hexdump').on('input propertychange paste', function() {
                updateUtilsHex();
            });
            $("input").keypress(function(e){
                var charCode = !e.charCode ? e.which : e.charCode;
                var c = String.fromCharCode(charCode);
                if(cp437.decode(c) < 0)
                    e.preventDefault();
            });
        });