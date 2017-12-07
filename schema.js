var gameSchema = mongoose.Schema({
    data             : {
        // Required Fields
        title        : String,
        permalink    : String, // A.K.A. slug
        developer    : String, // Should(can) point to user
        typetag      : String,
        platform     : String,
        rom          : String,
        screenshots  : [String],

        // Optional Fields
        license      : String,
        assetLicense : String,
        description  : String,
        video        : String,
        date         : Date,
        tags         : [String],
        alias        : [String],
        repository   : String,
        gameWebsite  : String,
        devWebsite   : String,
        onlineplay   : Boolean

    }
});