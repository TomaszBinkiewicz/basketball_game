$(document).ready(() => {

    let game_id = $('form').find('#game_id').val();
    // Adding points & stats
    let team_home = $("div#div_team1");
    let team_away = $("div#div_team2");
    let team_home_score = team_home.find("#team_home_score");
    let team_away_score = team_away.find("#team_away_score");
    let team_home_score_total = team_home.find("#team_home_score_total");
    let team_away_score_total = team_away.find("#team_away_score_total");
    let buttons_home = team_home.find("button");
    let buttons_away = team_away.find("button");
    team_home_score.val(0);
    team_away_score.val(0);


    let oldURL = document.referrer;
    // accessing data from db at the start of each game part

    $.ajax({
        url: "/get-team-stats/",
        data: {
            "game_id": game_id,
            "team": "home",
        },
        type: "GET",
        dataType: "json",
        success: function (data) {
            for (let property in data) {
                let element = team_home.find(`p.${property}`);
                element.text(data[property]);
            }
            let total_score = parseInt(data["3Pm"]) * 3 + parseInt(data["2Pm"]) * 2 + parseInt(data["FTm"]);
            team_home_score_total.val(total_score);
        },
        error: function (data) {
            if (oldURL === 'http://127.0.0.1:8000/new-game/'){
                console.log('redirected from http://127.0.0.1:8000/new-game/');
            } else {
                alert('error loading home team stats');
            }
        }
    });

    $.ajax({
        url: "/get-team-stats/",
        data: {
            "game_id": game_id,
            "team": "away",
        },
        type: "GET",
        dataType: "json",
        success: function (data) {
            for (let property in data) {
                let element = team_away.find(`p.${property}`);
                element.text(data[property]);
            }
            let total_score = parseInt(data["3Pm"]) * 3 + parseInt(data["2Pm"]) * 2 + parseInt(data["FTm"]);
            team_away_score_total.val(total_score);
        },
        error: function (data) {
            if (oldURL === 'http://127.0.0.1:8000/new-game/'){
                console.log('redirected from http://127.0.0.1:8000/new-game/');
            } else {
                alert('error loading guest team stats');
            }
        }
    });

    // reaction to buttons
    buttons_home.on("click", function (event) {
        event.preventDefault();
        let home_score = parseInt(team_home_score.val());
        let home_score_total = parseInt(team_home_score_total.val());
        if (isNaN(home_score_total)) {
            home_score_total = 0;
        }
        if (this.parentElement.parentElement.className === 'team_stats_points') {
            let add = parseInt($(this).val());
            home_score += add;
            home_score_total += add;
            team_home_score.val(home_score);
            team_home_score_total.val(home_score_total);
        }
        let class_name = this.className;
        let corresponding_field = $(this).parent().parent().siblings().find(`.${class_name}`);
        if (corresponding_field.length === 2) {
            let current0 = parseInt(corresponding_field.eq(0).text()) + 1;
            let current1 = parseInt(corresponding_field.eq(1).text()) + 1;
            corresponding_field.eq(0).text(current0);
            corresponding_field.eq(1).text(current1);
        } else {
            let current = parseInt(corresponding_field.text()) + 1;
            corresponding_field.text(current);
        }

        // saving atats
        let csrf_token = $('[name=csrfmiddlewaretoken]');
        $.ajax({
            url: "/save-team-stats/",
            data: {
                "csrfmiddlewaretoken": csrf_token.val(),
                "game_id": game_id,
                "stat_name": class_name,
                "team": "home",
            },
            type: "POST",
            dataType: "json",
            success: function (data) {
                console.log('succsess');
            },
            error: function (data) {
                alert('server connection denied');
            }
        });
    });

    buttons_away.on("click", function (event) {
        event.preventDefault();
        let away_score = parseInt(team_away_score.val());
        let away_score_total = parseInt(team_away_score_total.val());
        if (isNaN(away_score_total)) {
            away_score_total = 0;
        }
        if (this.parentElement.parentElement.className === 'team_stats_points') {
            let add = parseInt($(this).val());
            away_score += add;
            away_score_total += add;
            team_away_score.val(away_score);
            team_away_score_total.val(away_score_total);
        }
        let class_name = this.className;
        let corresponding_field = $(this).parent().parent().next().find(`.${class_name}`);
        if (corresponding_field.length === 2) {
            let current0 = parseInt(corresponding_field.eq(0).text()) + 1;
            let current1 = parseInt(corresponding_field.eq(1).text()) + 1;
            corresponding_field.eq(0).text(current0);
            corresponding_field.eq(1).text(current1);
        } else {
            let current = parseInt(corresponding_field.text()) + 1;
            corresponding_field.text(current);
        }

        // saving atats
        let csrf_token = $('[name=csrfmiddlewaretoken]');
        $.ajax({
            url: "/save-team-stats/",
            data: {
                "csrfmiddlewaretoken": csrf_token.val(),
                "game_id": game_id,
                "stat_name": class_name,
                "team": "away",
            },
            type: "POST",
            dataType: "json",
            success: function (data) {
                console.log('succsess');
            },
            error: function (data) {
                alert('server connection denied')
            }
        });
    });

});