const db = require('./config/db');

async function updateSchema() {
    try {
        console.log("Checking for leaderboard_name column...");
        const result = await db.query(`
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='users' AND column_name='leaderboard_name'
        `);
        
        if (result.rows.length === 0) {
            console.log("Adding leaderboard_name column...");
            await db.query("ALTER TABLE users ADD COLUMN leaderboard_name VARCHAR(50)");
            console.log("Column added successfully.");
        } else {
            console.log("Column already exists.");
        }
    } catch (err) {
        console.error("Error updating schema:", err);
    } finally {
        process.exit();
    }
}

updateSchema();
