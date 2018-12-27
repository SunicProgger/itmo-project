var usermenu = 0;
var shipforedit;

$(document).ready(function() {
	$('#search-person').on("input", function() {
		$('#add-p-block').hide();
		var poisk = $(this).val().toLowerCase();
		if (poisk.length > 0) {
			$('.person-block').each(function() {
				var person = $(this);
				person.find('span').each(function() {
					var name = $(this).text();
					var i = name.toLowerCase().indexOf(poisk);
					if (i + 1) {
						var up = name.substr(i, poisk.length);
						var span = '<span style="background: #ffff00;">' + up + '</span>';
						var rename = name.replace(up, span);
						$(this).html(rename);
						person.parent().show();
						return false;
					} else {
						$(this).find('span').each(function() {						
							$(this).css('background', 'rgba(0,0,0,0)');
						})
						person.parent().hide();
					}
				});
			});
		} else {
			$('.person-block').each(function() {
				var person = $(this);
				person.find('span').each(function() {
					$(this).css('background', 'rgba(0,0,0,0)');
				});
				$(this).parent().show();
			});
		}
	});
	$('#search-co').on("input", function() {
		var poisk = $(this).val().toLowerCase();
		$('#add-co-block').hide();
		$('#addcompany').show();
		if (poisk.length > 0) {
			$('.admincodata').each(function() {
				$(this).height("100%");
				$(this).children('.co-scroll').rotate(180);
				var co = $(this);var k = 0;
				co.find('span').each(function() {
					var name = $(this).text();
					var i = name.toLowerCase().indexOf(poisk);
					if (i + 1) {
						var up = name.substr(i, poisk.length);
						var span = '<span style="background: #ffff00;">' + up + '</span>';
						var rename = name.replace(up, span);
						$(this).html(rename);
						k = k + 1;
					} else {
						$(this).find('span').each(function() {						
							$(this).css('background', 'rgba(0,0,0,0)');
						});
					}
				});
				if (k == 0) {
					co.hide();
				} else {
					co.show();
				}
			});
		} else {
			console.log('1');
			$('.admincodata').each(function() {
				$(this).show();
				$(this).height("36px");
				$(this).find('span').each(function() {						
					$(this).css('background', 'rgba(0,0,0,0)');
				});
				$(this).children('.co-scroll').rotate(0);
			});
		}
	});
});

$('#companynamewrapper').click(function() {
	if (usermenu == 0) {
		$('#companynamefun').css('height','100%');
		usermenu = 1;
	} else {
		$('#companynamefun').css('height','0');
		usermenu = 0;
	}
});

$('#head-block').mouseover(function() {
	$('#companynamefun').css('height','100%');
})
$('#head-block').mouseout(function() {
	$('#companynamefun').css('height','0');
})

function delshipalert(name, id) {
	html = '<div id="delshipalertdiv" class="my-auto mx-auto" style="z-index: 101;position: relative;display: block;width: 350px;height: 200px;top: 200px;border: 2px solid #522302;border-radius: 20px;background-color: rgba(222,146,0,1);padding: 5px;"><span style="margin-top: 10px;margin-left: 10px;font-size: 20px;color: #522302;">Вы уверены, что хотите удалить из системы судно "';
	html += name;
	html += '"?</span><a href="delship_';
	html += id;
	html += '"><button class="btn btn-danger" style="position: absolute;bottom: 20px;left: 40px;font-size: 20px;">Удалить</button></a><button class="btn btn-info" onclick="closeshipalert();" style="position: absolute;bottom: 20px;right: 40px;font-size: 20px;">Отмена</button></div>';
	$('#delshipalert').html(html);
	$('#delshipalert').show();
}

function closeshipalert() {
	$('#delshipalert').hide();
}

function delcoalert(name, id) {
	html = '<div id="delcoalertdiv" class="my-auto mx-auto" style="z-index: 101;position: relative;display: block;width: 350px;height: 200px;top: 200px;border: 2px solid #522302;border-radius: 20px;background-color: rgba(222,146,0,1);padding: 5px;"><span style="margin-top: 10px;margin-left: 10px;font-size: 20px;color: #522302;">Вы уверены, что хотите удалить из системы компанию "';
	html += name;
	html += '"?</span><a href="delco_';
	html += id;
	html += '"><button class="btn btn-danger" style="position: absolute;bottom: 20px;left: 40px;font-size: 20px;">Удалить</button></a><button class="btn btn-info" onclick="closecoalert();" style="position: absolute;bottom: 20px;right: 40px;font-size: 20px;">Отмена</button></div>';
	$('#delcoalert').html(html);
	$('#delcoalert').show();
}

function closecoalert() {
	$('#delcoalert').hide();
}

jQuery.fn.rotate = function(degrees) {
    $(this).css({'transform' : 'rotate('+ degrees +'deg)'});
    return $(this);
};

$('#open-add-ship').click(function() {
	$(this).hide();
	$('#add_ship').css('height', '500px');
	$('#edit-ship-block').hide();
});

$('#add-ship-close-button').click(function() {
	$('#add_ship').css('height', '65px');
	$('#open-add-ship').show();
});

$('#add-p-block-show').click(function() {
	if ($('#add-p-block').css('display') == "none") {
		$('#add-p-block').slideDown();
	} else {
		$('#add-p-block').slideUp();
	}
});

$('.co-scroll').click(function() {
	if ($(this).parent($('.admindata')).css('height') == "40px") {
    	$(this).rotate(180);
		$(this).parent($('.admindata')).css('height', '100%');
	} else {
    	$(this).rotate(0);
		$(this).parent($('.admindata')).css('height', '40px');
	}
});

$('.block-edit-top').click(function() {
	var ship = $(this).parent();
	shipforedit = ship;
	var name = ship.find('.ship-name-for-edit').text();
	var model = ship.find('.ship-model-for-edit').text();
	var date = ship.find('.ship-date-for-edit').text();
	var title = ship.find('.ship-title-for-edit').text();
	var id = ship.find('.ship-id-for-edit').text(); 
	$('#editshipname').val(name);
	$('#editshipmodel').val(model);
	$('#editshipdate').val(date);
	$('#editshiptitle').text(title);
	$('#editshipid').val(id);
	shipforedit.hide();
	$('#edit-ship-block').show();
	$('#add_ship').css('height', '65px');
	$('#open-add-ship').show();
	window.scrollTo(0, $('body').height());
});

$('#block-edit-co-top').click(function() {
	$('.co-info-1').hide();
	$('.co-info-2').show();
	$('.co-info-1').parent().css('border-bottom', 'none');
	$('.co-info-2').parent().css('border-bottom', '1px solid #522302');
});
$('#edit-co-back').click(function() {
	$('.co-info-2').hide();
	$('.co-info-1').show();
	$('.co-info-2').parent().css('border-bottom', 'none');
	$('.co-info-1').parent().css('border-bottom', '1px solid #522302');
});

$('#edit-ship-close-button').click(function() {
	$('#edit-ship-block').hide();
	shipforedit.show();
});

$('#addcompany').click(function() {
	$('#add-co-block').show();
	$('.admincodata').each(function() {
		$(this).hide();
	});
	$(this).hide();
});

$('#add-co-btn-close').click(function() {
	$('#addcompany').show();
	$('#add-co-block').hide();
	$('.admincodata').each(function() {
		$(this).show();
	});
})