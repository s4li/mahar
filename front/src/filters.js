import Vue from 'vue'

Vue.filter('faNum', function (value) {
  let outputString = []
  let chrCode, chr
  value = String(value)
  for (var i = 0; i < value.length; i++) {
    chrCode = value.charCodeAt(i)
    chr = value.charAt(i)
    if(chrCode>47 && chrCode<58) chr = String.fromCharCode(chrCode+1728)
    outputString.push(chr)
  }
  return outputString.join('');
})
Vue.filter('tooman', function (value) {
  let result = ""
  if (value !== undefined) result = value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".") + " تومان"
  return result
})
Vue.filter('truncate', function (value) {
  let shortText = value.slice(0, 250)
  if (value.length>300) shortText += "..."
  return shortText
})