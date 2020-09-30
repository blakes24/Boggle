$(async function() {
	$guessForm = $('#guess-form');
	BASE_URL = 'http://127.0.0.1:5000';
	score = 0;
	time = 60;
	words = [];

	timer(time);

	$guessForm.on('submit', async function(evt) {
		evt.preventDefault(); // no page-refresh on submit

		$('#msg').text('');
		let guess = $('#guess').val();
		if (words.includes(guess)) {
			$('#msg').text(`${guess} already played`);
			$('#guess').val('');
			return;
		}
		const res = await axios.get(`${BASE_URL}/check`, { params: { guess: guess } });
		msg = res.data['result'];
		if (msg === 'ok') {
			postScore(guess);
			addWord(guess);
		} else {
			$('#msg').text(`${guess} is ${msg}`);
		}
		$('#guess').val('');
	});

	function postScore(word) {
		points = word.length;
		score += points;
		$('#score').text(`Score:${score}`);
	}

	function addWord(word) {
		words.push(word);
		$('#words').append(`<li>${word}</li>`);
	}

	function timer(time) {
		count = setInterval(function() {
			time -= 1;
			$('#timer').text(`timer:${time}`);
			if (time === 0) {
				clearInterval(count);
				alert("Time's Up!");
				$('input[type="submit"]').prop('disabled', true);
			}
		}, 1000);
	}
});
