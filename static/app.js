class BoggleGame {
	constructor(time) {
		this.time = time;
		this.words = [];
		this.score = 0;
		this.timer = setInterval(this.countDown.bind(this), 1000);

		$('#guess-form').on('submit', this.submitWord.bind(this));
	}

	postScore(word) {
		let points = word.length;
		this.score += points;
		$('#score').text(this.score);
	}

	addWord(word) {
		this.words.push(word);
		$('#words').append(`<li>${word}</li>`);
	}

	async countDown() {
		this.time -= 1;
		$('#timer').text(this.time);
		if (this.time === 0) {
			clearInterval(this.timer);
			$('#guess-form').hide();
			let msg = await this.sendScore();
			alert("Time's Up!");
			alert(`${msg} ${this.score}`);
		}
	}

	async submitWord(evt) {
		evt.preventDefault(); // no page-refresh on submit

		$('#msg').text('');
		let guess = $('#guess').val();

		if (this.words) {
			if (this.words.includes(guess)) {
				$('#msg').text(`${guess} already played`);
				$('#guess').val('');
				return;
			}
		}
		const res = await axios.get('/check', { params: { guess: guess } });
		let msg = res.data['result'];
		if (msg === 'ok') {
			this.postScore(guess);
			this.addWord(guess);
		} else {
			$('#msg').text(`${guess} is ${msg}`);
		}
		$('#guess').val('');
	}

	async sendScore() {
		const res = await axios.post('/score', { score: this.score });
		let msg = res.data['msg'];
		let high = res.data['high'];
		$('#high-score').text(high);
		return msg;
	}
}

let game = new BoggleGame(60);
