$.getJSON('/get_data', function(data) {
  var today = new Date();
  console.log("Data fetched:", data);  // Log the fetched data

  // Parse date strings into Date objects
  data.forEach(function(item) {
      item.date = new Date(item.date);
  });

  // Call your data processing function
  refreshNotifications(data, today);
  
  console.log("Data processed, redirecting...");  // Log before redirection
  // Redirect to the home page after processing the data
  // window.location.href = '/get_data';
}).fail(function(jqxhr, textStatus, error) {
  console.error("Request Failed:", textStatus, error);  // Log any errors
});

function refreshNotifications(items, today) {
  items = items || [];
  today = today || newDate();
  
  var cssTransitionEnd = getTransitionEnd();
  var container = $('#navbarColor03');
  
  items.forEach(function(item) {
    item.isExpired = item.date < today;
    
    item.isToday = (item.date.getFullYear() === today.getFullYear()) &&
      (item.date.getMonth() === today.getMonth()) &&
      (item.date.getDate() === today.getDate());    
    
    item.formattedDate = function() {
      if (this.isToday) {
        return timeToString(this.date);
      } else {
        return this.date.getFullYear() + '-' +
          strpad(this.date.getMonth() + 1) + '-' +
          strpad(this.date.getDate());
      }
    };
  });
  
  items.sort(function(a, b) {
    if (a.isExpired === b.isExpired) {
      return a.date - b.date;
    } else {
      return (b.isExpired ? 0 : 1) - (a.isExpired ? 0 : 1);
    }
  });
  
  var template = 
      '<div class="notifications js-notifications">' +
        '<h3>Notifications</h3>' +
        '<ul class="notifications-list">' +
          '<li class="item no-data">You don\'t have notifications</li>' +
          '{{#items}}' +
            '<li class="item js-item {{#isExpired}}expired{{/isExpired}}" data-id="{{id}}">' +
              '<div class="details">' +
                '<a href= "{{href}}">'+
                '<span class="Title">{{title}}</span>' +
                '<span class="date">{{formattedDate}}</span>' +
                '</a>'+
              '</div>' +
              '<button type="button" class="button-default button-dismiss js-dismiss">×</button>' +
            '</li>' +
          '{{/items}}' +
        '</ul>' +
      '</div>';
  
  container
    .append(Mustache.render(template, { items: items }))
    .find('.js-count').attr('data-count', items.length).html(items.length).end()
    .on('click', '.js-show-notifications', function (event) {
      $(event.currentTarget).closest('.js-show-notifications').toggleClass('active').blur();
      return true;
    })
    .on('click', '.js-dismiss', function (event) {
      var item = $(event.currentTarget).parents('.js-item');

      var removeItem = function () {
        item[0].removeEventListener(cssTransitionEnd, removeItem, false);
        item.remove();

        /* update notifications' counter */
        var countElement = container.find('.js-count');
        var prevCount = +countElement.attr('data-count');
        var newCount = prevCount - 1;
        countElement
          .attr('data-count', newCount)
          .html(newCount);

        if (newCount === 0) {
          countElement.remove();
          container.find('.js-notifications').addClass('empty');
        }
      };

      item[0].addEventListener(cssTransitionEnd, removeItem, false);
      item.addClass('dismissed');
      return true;
    });
}


function randomDate(start, end) {
  start = start || (new Date(2021, 0, 1));
  end = end || (new Date(2022, 0, 1));
  return new Date(start.getTime() + Math.random() * (end.getTime() - start.getTime()));
}

function addMinutes(date, minutes) {
  return new Date(date.getTime() + minutes * 60000);
}

function timeToString(date) {
  if (date) {
    var hh = date.getHours();
    var mm = date.getMinutes();
    var ap = hh >= 12 ? 'PM' : 'AM';

    hh = (hh >= 12) ? (hh - 12) : hh;
    hh = (hh === 0) ? 12 : hh;

    return (hh < 10 ? '0' : '') + hh.toString() + ':' +
      (mm < 10 ? '0' : '') + mm.toString() + ' ' + ap;
  }
  return null;
}

function strpad(num) {
  if (parseInt(num) < 10) {
    return '0' + parseInt(num);
  } else {
    return parseInt(num);
  }
}

function getTransitionEnd() {
  var supportedStyles = window.document.createElement('fake').style;
  var properties = {
    'webkitTransition': { 'end': 'webkitTransitionEnd' },
    'oTransition': { 'end': 'oTransitionEnd' },
    'msTransition': { 'end': 'msTransitionEnd' },
    'transition': { 'end': 'transitionend' }
  };
  
  var match = null;
  Object.getOwnPropertyNames(properties).forEach(function(name) {
    if (!match && name in supportedStyles) {
      match = name;
      return;
    }
  });
  
  return (properties[match] || {}).end;
}