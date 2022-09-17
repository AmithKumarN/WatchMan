const mongoose = require("mongoose");

const Schema = mongoose.Schema;

const statsSchema = new Schema({
    ip: { type: String, required: true},
    hostname: { type: String, required: true},
    date: { type: Date, required: true},
    cpu: { type: Number, required: true},
    memory: { type: Number, required: true},
    disk: { type: Number, required: true}
}, {
    versionKey: false
});

const Stats = mongoose.model('Stats', statsSchema);

module.exports = Stats;