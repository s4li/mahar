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
Vue.filter('translate', function (value) {
  let Text;
  if (value == 1) {
    Text = 'هفتم'
  } else if (value == 2) {
      Text = 'هشتم'
  } else if (value == 3) {
      Text = 'نهم'
  } else if (value == 5) {
      Text = 'دهم'
  } else if (value == 6) {
      Text = 'یازدهم'
  } else if (value == 7) {
      Text = 'دوازدهم'
  }
return Text
})