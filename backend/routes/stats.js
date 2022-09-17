const router = require('express').Router();
let Stats = require('../models/stats.model');

router.route('/').get((req, res) => {
    Stats.find()
        .then(stats => res.json(stats))
        .catch(err => res.status(400).json('Error: ' + err));
});

router.route('/add').post((req, res) => {
    const ip = req.body.ip;
    const hostname = req.body.hostname;
    const date = Date.parse(req.body.date);
    const cpu = Number(req.body.cpu);
    const memory = Number(req.body.memory);
    const disk = Number(req.body.disk);

    const newStat = new Stats({
        ip,
        hostname,
        date,
        cpu,
        memory,
        disk
    });

    newStat.save()
        .then(() => res.json('Stat added!'))
        .catch(err => res.status(400).json('Error: ' + err));
});

module.exports = router;