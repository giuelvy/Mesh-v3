
// CPAGrip postback trigger
const CPAGRIP_KEY = "REPLACE_KEY";
function onFormSubmit(e){
  var email = e.namedValues['Email'][0];
  var ip = (e.namedValues['IP']||[''])[0];
  var url = 'https://postback.cpagrip.com/?key='+CPAGRIP_KEY+'&subid='+encodeURIComponent(email)+'&subid2='+encodeURIComponent(ip);
  UrlFetchApp.fetch(url, {muteHttpExceptions:true});
}
