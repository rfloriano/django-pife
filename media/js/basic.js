function flipCard(img, id){
    $("#flipped-div").html('<img class="draggable-card" src="'+ img +'" id="flipped" name="'+ id +'"/>');
}

function toGarbageCard(img, id){
    $("#garbage").html('<img class="ui-draggable draggable-card trash" src="'+ img +'" id="'+ id +'" name="'+ id +'"/>');
}

function canFlipCard(){
    if (deck_enabled){
        Dajaxice.pife.next_card('Dajax.process');
        trash_can_get = false;
    }
}

function addCard(id){
    cards.push(id);
}

function removeCard(id){
    cards.splice(cards.indexOf(id), 1);
}

function init(){
	$( ".draggable-card, .draggable-mycard, .draggable-trash, .draggable-pife" ).draggable();
}

function changeClass(el, oldClass, newClass){
    el.addClass(newClass);
    el.removeClass(oldClass);
}

$(function() {
    init();
    $( ".droppable-game" ).droppable({
        accept: ".draggable-mycard",
        activeClass: "shadow-hover",
        hoverClass: "ui-state-active",
        drop: function( event, ui ) {
            $(this).append($(ui.draggable));
            $(ui.draggable).css("top", "0px");
            $(ui.draggable).css("left", "0px");
            $(ui.draggable).addClass("draggable-card");
            $(ui.draggable).addClass("draggable-group");

//            $(ui.draggable).parent().children();
        }
    });
    $( "#garbage" ).droppable({
        accept: ".draggable-mycard",
        activeClass: "shadow-hover",
        hoverClass: "ui-state-active",
        drop: function( event, ui ) {
            if (trash_enabled){
                $("#garbage").append($(ui.draggable));
                $(ui.draggable).css("top", "0px");
                $(ui.draggable).css("left", "0px");
                Dajaxice.pife.trash_card('Dajax.process', {'card': $(ui.draggable).attr('id')});
                $(ui.draggable).attr("id", "trash");
                changeClass($(ui.draggable), "draggable-mycard", "draggable-card");
                deck_enabled = true;
                trash_enabled = false;
                if ($(ui.draggable).hasClass("draggable-group"))
                    $(ui.draggable).removeClass("draggable-group");
                removeCard($(ui.draggable).attr("name"));
            }else{
                $(ui.draggable).draggable({ revert: "valid" });
            }
        }
    });
    $( "#my-game" ).droppable({
        accept: ".draggable-card",
        activeClass: "shadow-hover",
        hoverClass: "ui-state-active",
        drop: function( event, ui ) {
            if (deck_enabled){
                // se a carta vir do bolo para o meu jogo
                // TODO: Validar se o cara pega uma carta do bolo e pega do lixo
                $("#my-game").append($(ui.draggable));
                changeClass($(ui.draggable), "draggable-card", "draggable-mycard");
                $(ui.draggable).css("top", "0px");
                $(ui.draggable).css("left", "0px");
                is_trash = $(ui.draggable).attr("id") == "trash";
                Dajaxice.pife.get_card('Dajax.process', {'card': $(ui.draggable).attr("name"),'trash': is_trash});
                $(ui.draggable).attr("id", $(ui.draggable).attr("name"));
                if (!$(ui.draggable).hasClass("draggable-group")){
                    deck_enabled = false;
                    trash_enabled = true;
                    if ($(ui.draggable).hasClass('trash') && trash_can_get){
                        (ui.draggable).removeClass('trash');
                        Dajaxice.pife.gotted_trash('Dajax.process');
                    }else{
                        $(ui.draggable).draggable({ revert: "valid" });
                    }
                }else{
                    $(ui.draggable).removeClass("draggable-group");
                }
                addCard($(ui.draggable).attr("name"));
            }else if (trash_enabled && !deck_enabled && $(ui.draggable).attr("id") == "trash"){
                // se a carta vir da lixeira para o meu jogo
                alert("gotted");
                trash_enabled = $(ui.draggable).attr('name');
                addCard($(ui.draggable).attr("name"));
                $(ui.draggable).attr("id", trashsh_enabled);
            }else{
                // se a carta vir dos jogos "baixados" (grupos) para o meu jogo
                $("#my-game").append($(ui.draggable));
                changeClass($(ui.draggable), "draggable-card", "draggable-mycard");
            }
        }
    });

    $("#bati").click(function(){
        group1 = [ $("#g1").children("img").attr("id"), $("#g2").children("img").attr("id"), $("#g3").children("img").attr("id") ];
        group2 = [ $("#g4").children("img").attr("id"), $("#g5").children("img").attr("id"), $("#g6").children("img").attr("id") ];
        group3 = [ $("#g7").children("img").attr("id"), $("#g8").children("img").attr("id"), $("#g9").children("img").attr("id") ];
        Dajaxice.pife.check_game('Dajax.process', {'group1': group1,'group2': group2,'group3': group3 });
    });

    $("#restart").click(function(){
        window.location = "/";
    })
});

