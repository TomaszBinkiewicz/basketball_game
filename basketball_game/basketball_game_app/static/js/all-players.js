$(document).ready(() => {

    let content_div = $('div.content-list')
    let select_field = content_div.find('#players-team');
    let players_list = content_div.find('ul');

    select_field.on("change", function (event) {
        if (this.value === "all") {
            window.location.href = `/all-players/`;
        } else {
            let team_id = parseInt(this.value);
            window.location.href = `/team-players/${team_id}`;
        }
    });

})
;