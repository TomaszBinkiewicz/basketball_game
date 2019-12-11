$(document).ready(() => {

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
    });


    // Saving stats
    let end_quarter_button = $('#end_quarter');

    end_quarter_button.on("click", function (event) {
        // TODO: save stats to db
        event.preventDefault();

        let home_3Pm = team_home.find("p.3Pm").eq(0).text();
        let home_2Pm = team_home.find("p.2Pm").eq(0).text();
        let home_FTm = team_home.find("p.FTm").eq(0).text();
        let home_3Pa = team_home.find("p.3Pa").eq(0).text();
        let home_2Pa = team_home.find("p.2Pa").eq(0).text();
        let home_FTa = team_home.find("p.FTa").eq(0).text();

        let home_OffReb = team_home.find("p.OffReb").eq(0).text();
        let home_DefReb = team_home.find("p.DefReb").eq(0).text();
        let home_Ast = team_home.find("p.Ast").eq(0).text();
        let home_Stl = team_home.find("p.Stl").eq(0).text();
        let home_Blk = team_home.find("p.Blk").eq(0).text();

        let home_Tov = team_home.find("p.Tov").eq(0).text();
        let home_PF = team_home.find("p.PF").eq(0).text();
        let home_TF = team_home.find("p.TF").eq(0).text();

        console.log(home_3Pm, home_2Pm, home_FTm, home_3Pa, home_2Pa, home_FTa);
        $.ajax({
            url: '/save-team-stats/',
            data: {
                "home_3Pm": home_3Pm,
                "home_2Pm": home_2Pm,
                "home_FTm": home_FTm,
                "home_3Pa": home_3Pa,
                "home_2Pa": home_2Pa,
                "home_FTa": home_FTa,
                "home_OffReb": home_OffReb,
                "home_DefReb": home_DefReb,
                "home_Ast": home_Ast,
                "home_Stl": home_Stl,
                "home_Blk": home_Blk,
                "home_Tov": home_Tov,
                "home_PF": home_PF,
                "home_TF": home_TF,
            },
            type: "POST",
            dataType: "json"
        }).fail(function(event){
            event.preventDefault();
        })
        // TODO: repeat for guest team
    });

});