$(document).ready(function() {
    function handleSelectChange(selectId, resultLinkId, suffix) {
        $("#" + selectId).change(function() {
            updateResult();
            var selectedOption = $(this).val();
            var selectedPrice = parseFloat($("#" + selectId + " option:selected").attr('price')) || 0;
            $.ajax({
                type: "POST",
                url: "/process-selection",
                data: { option: selectedOption },
                success: function(response) {
                    $("#" + resultLinkId).text(selectedPrice + "₴" + suffix);
                }
            });
        });
    }

    function updateResult() {
        var o_house = parseFloat($("#o_house option:selected").attr('price')) || 0;
        var o_people = parseFloat($("#o_people option:selected").attr('price')) || 0;
        var o_time = parseFloat($("#o_time option:selected").attr('price')) || 0;
        var o_transport = parseFloat($("#o_transport option:selected").attr('price')) || 0;
        var res_val1 = o_house * o_time;
        var res_val2 = res_val1 * o_people;
        var res_val3 = o_people * o_transport
        var total = res_val2 + res_val3;
    
        var formattedTotal = total + "₴";
        $("#resultLink4").text(formattedTotal).attr('value', formattedTotal);
    
        // Обновим также поле o_sum в форме
        $("#order_sum").val(formattedTotal);
    }

    handleSelectChange("o_house", "resultLink", "/доба");
    handleSelectChange("o_time", "resultLink5", "");
    handleSelectChange("o_people", "resultLink2", "");
    handleSelectChange("o_transport", "resultLink3", "");

    updateResult();
});

$(document).ready(function() {
    function updateSelectedElement(selectId, targetId, prefix) {
        var selectedOptionText = $(selectId + " option:selected").text().trim();
        var resultText = selectedOptionText === "Зробіть вибір:" ? "" : prefix + selectedOptionText;
        $(targetId).text(resultText);
    }

    $("#o_house, #o_time, #o_people, #o_transport").change(function() {
        var selectId = "#" + $(this).attr("id");
        var targetId = $(this).data("target");
        var prefix = $(this).data("prefix");
        updateSelectedElement(selectId, targetId, prefix);
    });

    $("#o_house, #o_time, #o_people, #o_transport").each(function() {
        var selectId = "#" + $(this).attr("id");
        var targetId = $(this).data("target");
        var prefix = $(this).data("prefix");
        updateSelectedElement(selectId, targetId, prefix);
    });
});
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("myForm").addEventListener("submit", function(event) {
        var houseValue = document.getElementById("o_house").value;
        var timeValue = document.getElementById("o_time").value;
        var peopleValue = document.getElementById("o_people").value;
        var transportValue = document.getElementById("o_transport").value;

        if (houseValue === "0" || timeValue === "0" || peopleValue === "0" || transportValue === "0") {
            alert("Будь ласка, заповніть всі поля");
            event.preventDefault(); // Предотвращаем отправку формы
        }
    });

    // Добавляем обработчики изменений в каждом из селектов
    document.getElementById("o_house").addEventListener("change", enableSubmitButton);
    document.getElementById("o_time").addEventListener("change", enableSubmitButton);
    document.getElementById("o_people").addEventListener("change", enableSubmitButton);
    document.getElementById("o_transport").addEventListener("change", enableSubmitButton);

    // Функция для проверки, нужно ли включить кнопку отправки формы
    function enableSubmitButton() {
        var houseValue = document.getElementById("o_house").value;
        var timeValue = document.getElementById("o_time").value;
        var peopleValue = document.getElementById("o_people").value;
        var transportValue = document.getElementById("o_transport").value;
        var submitButton = document.getElementById("submitButton");

        if (houseValue !== "0" && timeValue !== "0" && peopleValue !== "0" && transportValue !== "0") {
            submitButton.disabled = false; // Включаем кнопку, если все поля выбраны
        } else {
            submitButton.disabled = true; // Выключаем кнопку, если хотя бы одно поле не выбрано
        }
    }
});