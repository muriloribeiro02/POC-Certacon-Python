document.addEventListener('DOMContentLoaded', function(){
    document.getElementById("deleteForm").addEventListener("submit", function(event){
        event.preventDefault();
        if (verificarSelecao()) {
            removerLinhasSelecionadas();
        } else {
            alert("Selecione pelo menos um item para deletar.");
        }
    });
});

function verificarSelecao() {
    var selectedCheckboxes = document.querySelectorAll('input[name="selecionar[]"]:checked');
    return selectedCheckboxes.length > 0;
}

function removerLinhasSelecionadas() {
    var selectedCheckboxes = document.querySelectorAll('input[name="selecionar[]"]:checked');
    var selectedIds = Array.from(selectedCheckboxes).map(function(checkbox) {
        return checkbox.value;
    });
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/deletar-dados-da-tabela", true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            window.location.href = '/';
        }
    };
    xhr.send(JSON.stringify({selected_ids: selectedIds}));
}