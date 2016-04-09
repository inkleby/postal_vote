hide_state = false;

    if (hide_state == true) {
        $(".extended").hide();
        $('#master_expand_link').text("Show All Notes");
    } else {
        $('#master_expand_link').text("Hide All Notes");
        $(".expand-link").hide();
    };


    
// opens or closes all links
$('#master_expand').click(function(event){
    event.preventDefault();
    $(".extended").fadeToggle();
    hide_state = !hide_state;
    if (hide_state == true) {
        $('#master_expand_link').text("Show All Notes");
        $(".expand-link").slideDown();
    } else {
        $('#master_expand_link').text("Hide All Notes");
        $(".expand-link").slideUp();
    };
});

//at change in section changes top menu and hash changes
var waypoints = $('.section-anchor').waypoint(function(direction) {
    if (direction == "down") {
        id = $(this).attr('id');
    } else {
        id = $(this).attr('prev');
    };
    
    $("li").removeClass("active");
    $("#menu-" + id).addClass("active");
    $("#caret-menu-" + id).addClass("active");
    harmlessHashChange($("#" + id + ".anchor").attr('name'));
    adjustMenus(id);
}, {
  // offset very slightly the location of the section ahcor
  offset: function() {
    if ($(this).is(':visible') == true){
        return $(this).height() + 20;
    } else {
    return 0
    }
  },
  
  continuous:false}
  
);

//shows an individual note
$('.expand-link').click(function(event){
    event.preventDefault();
    $(this).fadeOut();
    id = $(this).attr('id');
    $("#" + id + ".extended").animate({ height: 'toggle', opacity: 'toggle' }, 'slow');
 });
 
//hides an individual note
 $('.hide-link').click(function(event){
    event.preventDefault();
    id = $(this).parent().parent().attr('id');
    $("#" + id + ".extended").animate({ height: 'toggle', opacity: 'toggle' }, 'slow');
    $("#" + id + ".expand-link").fadeIn();
 });
 
//show citation link as hovering over text
 $( ".content-row" ).hover(
  function() {
    id = $(this).attr('id')
    $('#' + id + ".cite-link" ).show();
  }, function() {
    id = $(this).attr('id')
    $('#' + id + ".cite-link" ).hide();
  }
);


function adjustMenus(id) {
    
//adjust what is visible in menus to just the nearby scope
    id = parseInt(id)
    bottombar = id - 1
    topbar = id + 2
    leftselect = bottombar - 10
    rightselect = topbar + 10
    //unhide correct items
    for(var i=bottombar, len=topbar+1; i < len; i++){
        $("#menu-"+i).removeClass("hide-item");
    }
    
    //hide incorrect items
    $(".top-menu-item:visible").each(function (){
    
        local = parseInt($(this).attr('item'))
        if (local == 0) {
            local = 1
        }
            if ((local <= bottombar) || (local > topbar)) {
                $(this).addClass("hide-item")
            }
        
    
    })
    // set the << button to the previous section
    if (id > 1) {
        prev_link = $('[section='+ bottombar +']').attr('href')
        $("a#menu-prev").show().attr("href",prev_link);
    } else {
        $("a#menu-prev").hide();
    }
    
    
    next_link = $('[section='+ (topbar + 1) +']')
    
    if (next_link.length > 0) {
        $("a#menu-next").show().attr("href",next_link.attr('href'));
    } else {
        $("a#menu-next").hide()
    }
}

function harmlessHashChange(newhash){
//changes the hash in the address bar without moving the page

    if (currently_moving == false) {

        $("a[name=temp]").each(function() {
            old = $(this).attr("temp_name")
            $(this).attr('name',old)
        })

        if (newhash != "temp" ) {
            if (typeof newhash == "undefined") {
                window.location.hash = "start";
            } else {
                existing = $('a[name="' + newhash + '"]')
                existing.attr('temp_name',newhash);
                existing.attr('name',"temp");
                window.location.hash = newhash;
                window.setTimeout(function() {existing.attr('name',newhash)},1);

            }
        }
    
    }
}

var currently_moving = false

function gotoTarget(target,addText){
    para_id = target.attr('name')
            
            if (addText && currently_moving == false) {
            currently_moving = true
            $("#" + para_id + ".side-bar").prepend( "<p>Entered Here</p>" )
            }
            $('html,body').scrollTop(target.offset().top - 60) //offsets for fixed header

            parent = $("#" + target.attr('parent') + ".anchor")
            harmlessHashChange(parent.attr('name'));
            $("#" + para_id + ".content-row").addClass("highlighted-content")
            window.setTimeout(function() {$("#" + para_id + ".content-row").removeClass("highlighted-content")},20000)
            currently_moving = false;
}

function gotoHash(hash,addText){
//decodes the clever hash function
      key_areas = hash.split(".") //0 - section, 1 paragraph, 2 - prime, 3 - start, 4-end
      key_areas[0] = key_areas[0].substring(1) //remove hash
      key_target = '[key=' + key_areas[2] +']'
      start_end = '[start_key=' + key_areas[3] +']' + '[end_key=' + key_areas[4] +']'
      start_para ='[start_key=' + key_areas[3] +']' + '[name=' + key_areas[1] +']'
      end_para = '[end_key=' + key_areas[4] +']' + '[name=' + key_areas[1] +']'
      start ='[start_key=' + key_areas[3] +']'
      end = '[end_key=' + key_areas[4] +']'
      para = '[name=' + key_areas[1] +']' + '[parent=' + key_areas[0] +']'
      section = '[section=' + key_areas[0] +']'
      options = [key_target,start_end,start_para,end_para,start,end,para,section]
      
      for(var i=0, len=options.length; i < len; i++){
          target = $(options[i]);
          if (target.length) {
            gotoTarget(target,addText);
            break;
          }
      }
      

}


 $(function() {
  $('a[href*=#]:not([href=#])').click(function() {
    if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') 
&& location.hostname == this.hostname && $(this).hasClass('cite-copy') == false) {
        var splits = this.hash.split(".")
        if (splits.length > 2) {
            return gotoHash(this.hash.slice(1),false);

        } else {
            new_hash = this.hash.slice(1)
            if (new_hash == "index") {
            if ($("div#index").is(':visible') == false) {
                $("div#index").show()
                Waypoint.refreshAll()
            }
            } else {
                if ($("div#index").is(':visible') == true) {
                    $("div#index").hide()
                    Waypoint.refreshAll()
                }
            }
            $('html,body').scrollTop($('a[name="' + new_hash + '"]').offset().top - 60)
            return false
            }
      
      
    } else {
    return false;
    }
  });
  
function citeBox(dialog_title,link){
    //generates pretty citation box
    title = $("body").attr("title")
    full_title = $("body").attr("full-title")
    cite_author = $("body").attr("cite-author")
    year = $("body").attr("year")
    swal({
    title: dialog_title,
    text: '<a href="' + link+ '">' + title + ': Paragraph '+ $(this).attr("id") + '</a>' + 
    '<br><br>Cite As:<br><span class="cite"> ' + cite_author + '. (2015). '+ full_title + '. [online] Inkleby. Available at: '+ link + ' [Accessed 5 Oct. 2015]</span>',
    html: true,
    confirmButtonText: "OK" });
}
  
 //copies link to clipboard - disables further activity
$(".cite-copy").click(function(e) {
    var link = $(this).attr("href")

    
    clipboard.copy(link).then(
      function(){citeBox("Link added to Clipboard!",link);},
      function(err){citeBox("Copy Link From Below!",link);})
  

    e.stopPropagation();
});
 
  


$(window).load(function() {


      //Executed on page load with URL containing an anchor tag.
      if($(location.href.split("#")[1])) {
          var hash = '#'+location.href.split("#")[1];
          return gotoHash(hash,true);
          }
        
    });


    function followHash() {
        //allows hash moves within a document
        var splits = location.hash.split(".")
        if (splits.length > 2) {
            gotoHash(location.hash);
            }
    }

    window.onhashchange = followHash;


});

