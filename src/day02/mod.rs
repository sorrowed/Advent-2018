const INPUT: [&str; 250] = ["lsrivfotzgdxpkefaqmuiygchj", "lsrivfotzqdxpkeraqmewygchj",
    "lsrivfotzbdepkenarjuwygchj", "lsrivfotwbdxpkeoaqmunygchj", "lsrijfotzbdxpkenwqmuyygchj",
    "lsrivfotzbdxpkensqsuwygcdj", "lsrivfotubdxpkenzqmuwyschj", "lsrjvwotzbdxpkenaqjuwygchj",
    "lsrtvfotzbdxpkeaaqmuqygchj", "lscivzotzbdxpkenaqmuwygcnj", "ddrivfotzbdxpkenlqmuwygchj",
    "jsrivfvtzbdxpkenaqmufygchj", "csrivfotzxdxpkenaqguwygchj", "lprivfbtzbqxpkenaqmuwygchj",
    "lsrnvfotzbnxpkenaqmuwygchk", "lsiivfotzbdhpkencqmuwygchj", "lsrivfotzbyxpkenaqmzwygchc",
    "lsjivfotqbdxpvenaqmuwygchj", "lsrivfotzbdxpkencqmuwvgqhj", "lsrivfotzhdxpqenaqouwygchj",
    "lsrivfytzbnxpkenaqmuwygcsj", "llrivfotzbdxpkenaqmuwynchd", "lsuivfotzbdxpnenaqmuwygchk",
    "lsrtvootnbdxpkenaqmuwygchj", "ysrivfotzcdxpkenaqmuwhgchj", "lsrivfotxbdxpkefgqmuwygchj",
    "lsrmvfotzbaxpkenaqmuwygfhj", "lsrivfothbyxpkxnaqmuwygchj", "isrivfotzbdxpkenaqmkwygcht",
    "lhrivfotzbdxpkbnfqmuwygchj", "lsrivfotzbmxpkenaqmuwbgdhj", "lsrivvotzbdxcoenaqmuwygchj",
    "ssrwvfotzbdjpkenaqmuwygchj", "lsrivfotgbwxpkenaqmhwygchj", "lsrivfotzbdxpkenaqcuhygcyj",
    "lcdivfotzbdxpkenaqmuwxgchj", "ysbivfotzbdxpkenaqmuwkgchj", "lsrivfltzbdxxkenaqcuwygchj",
    "lsrivfotzbdxpkgnaqmunegchj", "fsqpvfotzbdxpkenaqmuwygchj", "lsriifotzbcxpkenaqmubygchj",
    "lsrivfotzjdxpkenaqmugygcjj", "tsrikfotzbdxpkeneqmuwygchj", "larivfotzbdxpkenaqmwwygcpj",
    "larivfotzbdxpkenaqmuayrchj", "lsravfotzbdxpkdoaqmuwygchj", "lsrivfotzbixpkenaqvtwygchj",
    "lsrixfotnbdxtkenaqmuwygchj", "lsrirfotzbdxpkeneqmuwygchv", "lsrivfofzedxpkenaqmswygchj",
    "lwrivfotzvdxpkenaqmuwygfhj", "lsrivfotzbdapkenaqmuqygehj", "lsrizfotgbdxpkenaqjuwygchj",
    "lsrivioxzbdxpkanaqmuwygchj", "lsrivfmtzbdxpkgnaqmuwcgchj", "lsrivfotzbdxpkeaaqmuofgchj",
    "lsrivfotvbdxpkenuqmuwygcht", "lsrivfothcdxpkenaqouwygchj", "lsgivfotzbdxpkenawmuwygchi",
    "lsrigfotzbdxpmonaqmuwygchj", "lsrivfotzbdxrkfnaqmuwygcha", "lsrivfopobdxpkenaqmuwygchv",
    "lsrejfotzbdxpkvnaqmuwygchj", "lsrivfotzbdxplenqqmuwygchz", "lsmivfotzbdppkebaqmuwygchj",
    "lsrivfotubdipkewaqmuwygchj", "lsrivfodnbhxpkenaqmuwygchj", "lsrivfotzbdxpkenaqmkwzgshj",
    "lsrixfotzbdxpkensqmuwygohj", "lsdivfotzbdxpkenaqmuwagcwj", "lsrimfotzbdxpkenaqmuwygcyu",
    "asnivfotzbdxpkenaqmbwygchj", "lseivfltfbdxpkenaqmuwygchj", "lsrivfbtzbdxpuenaqmuwyychj",
    "lsziafozzbdxpkenaqmuwygchj", "lsrivfotzbdxpkwnaomuwygchg", "ldrivfotzbdxpkeniqmuwygihj",
    "lsrivfotzbdxpkenaqhdwycchj", "lsrigfotzbdxphenaqmuwynchj", "lsripfotzbdxpgenaqmuwygchh",
    "lsrgvfoczbdxpkenaqmuwygihj", "lsribfotzbgxpkenaqhuwygchj", "lsrkvfotztdxpienaqmuwygchj",
    "lsrivfohzbdxpkenaqrxwygchj", "lsrivfoszbdxpkenavmuwygvhj", "lsrivfstzblxpkcnaqmuwygchj",
    "lzrivfotzbdxpkegaqmuwygchv", "lsrivtotzbdxpkenaqrumygchj", "lsgivfotzbdwpkenaqmuwhgchj",
    "lurivfotybdxpkenaqmuwygchg", "lsrivfogzbdxpkmnrqmuwygchj", "lsrivgotzbdxpkengqmuwygcwj",
    "lirivfbyzbdxpkenaqmuwygchj", "lwrivfotzbdxpkbjaqmuwygchj", "lsrivkotzbqxakenaqmuwygchj",
    "lxrivfotzbdxpkenaqmuwygshy", "lxxivfqtzbdxpkenaqmuwygchj", "lsrivfohzbdxpzenaqmuzygchj",
    "lsrivfotzndxekenaqmuwygcvj", "lsrdvfotzbdxpkenaqguiygchj", "lsrivfotzbdxpiehaqauwygchj",
    "atrivfotzbdxpkenaqmuwygchz", "lsrivfovzbdxpkenaqmuvygcwj", "lsrivfotzmdxpkennqmuwyxchj",
    "luvcvfotzbdxpkenaqmuwygchj", "lsriqfotzbdxpbenaqmuwygchg", "bsoivfotzudxpkenaqmuwygchj",
    "lsrivfotzbdxphenaqmhwxgchj", "lsrivfotzbdxpkenasmuwjgchw", "lsrivdotzboxpkenaqmuwykchj",
    "lsqivfotzbdxcdenaqmuwygchj", "lsrivfktzndypkenaqmuwygchj", "lwrivfotzbdxpkenaqmuolgchj",
    "lkrivfowzbdxpkenaqmbwygchj", "lsrivhotzbdxpkenaqyuwygvhj", "lsruvfotzbdxpkecaqmukygchj",
    "lsrivdotzbdsskenaqmuwygchj", "lsrivfotzbdxpkanaqmuwygcmc", "lsrgvfotubdxpkenrqmuwygchj",
    "psrivfotzbdxpkenaqmutygchd", "lsrivfitzbdxpkenagmiwygchj", "lsrivfotzbdxpkbnaqauwyrchj",
    "lsrivfotvbdxpjenaqmuwygchr", "lsrdvfoyzbjxpkenaqmuwygchj", "vsrivfothbdxpkenaqmuwyychj",
    "lyrivfotzpdxpkepaqmuwygchj", "lsgbqfotzbdxpkenaqmuwygchj", "lxrivfotzbdxpkenegmuwygchj",
    "lsrivfokzbdxpkenaqnuwyxchj", "lsrivfotubmxpkexaqmuwygchj", "lswivfvtzbdxpkenaqmuwygcgj",
    "lsrivfonzbdxpkenaqiuwygchc", "isrivlotzbdxpkenaqmuwygchf", "lsrilfozzbdxpkenaqmuwygcvj",
    "wsrivfotzbdxpkepaqmuwegchj", "lsrivfrtzbrxpkenaqquwygchj", "lsrivfotzbdxpkeqaqmuoygjhj",
    "lsrivfotzmdxpkenaqmuwyxchg", "lsrnvfotzbzxxkenaqmuwygchj", "ldrivfotzbdxpkenaqmlxygchj",
    "lsriofotzbdxpkenaqmwwmgchj", "lsrivfotzodxjkenaqmuwyglhj", "lsriviotzbdxpkegaqguwygchj",
    "lsrimfotzbdxpkanaqmuwygshj", "lwrzvfotzbdxpkenaqmuwygcfj", "lirivfotzbdxkkenvqmuwygchj",
    "lsrivfotlbdxpkeoaqmuwygahj", "lsxivfotzbdxpkenaqmuwwgchi", "lsrivfotzbdxpkenaqmukygzzj",
    "lsrtvfotzbdxskenaqmuwygcij", "lsgilfotzbdxpdenaqmuwygchj", "lsriyfotbbdxpkenaqmuwygchm",
    "lsrivfotabdxpkenaqmuwyghhs", "xsrizfotzbdxpkenaqmuwygczj", "lsrivfotybdxpkenaqquwygchx",
    "lsrzvfofzbdxpktnaqmuwygchj", "xsripfotzbdxpkenaqmqwygchj", "lsrivfotzbdspkenahmuwugchj",
    "lsmivfotzbdbpkenaqmuwygchy", "lsruvfotzbdxpkenaqqpwygchj", "lrmivfotzbdxpkenaqguwygchj",
    "lsnivfotzbdlpketaqmuwygchj", "lsrivfotzbdxjketaqjuwygchj", "lsrivxotzbdchkenaqmuwygchj",
    "lsrivootzbdxpkenaqmuwybmhj", "tsrivfdtzbdxpkenaqmuwpgchj", "lsrivmotzbdxpkxnaqmuwcgchj",
    "lsrivfotzadepkenaqmuwyichj", "dsrivfotrbdxpkenaqmuwtgchj", "lsrivfhtzbdxvkenoqmuwygchj",
    "lsrivfotzvdxbkenaqmbwygchj", "lsrxvcotzbdxpkenaqmuwygvhj", "lsrivfotzbdxykenaqmuwfgcha",
    "lsbivfotzbdxpkenaqmuwfvchj", "lfrivfotzbdcpkgnaqmuwygchj", "lsrivfotzbdxpwegdqmuwygchj",
    "lsrivfotyjdupkenaqmuwygchj", "gsrivfotzbdxpkenaemuwcgchj", "lsrivfodqbdxpkenaqmuwygchg",
    "lsrivfoczbdxpkenaqnuwwgchj", "lsrivpouzbhxpkenaqmuwygchj", "llbivuotzbdxpkenaqmuwygchj",
    "lfrivfofzbdxpkenaqmuwygchb", "lsrivfotzbdxpkenaumuwgghhj", "lsrivfotzbdxqaenazmuwygchj",
    "lsrivfotzbgxpkenkqmqwygchj", "lsrivfotzbdxpkensqiawygchj", "ljrijfotzbdxppenaqmuwygchj",
    "lsrivfoszbdxpkrnlqmuwygchj", "lsrijfotzbdxpcfnaqmuwygchj", "lsrivfotzbdopkebaqmuwytchj",
    "lsrivfonzbdxnkenalmuwygchj", "larivfouzbvxpkenaqmuwygchj", "lsryvfotzbdxpkensqmuwygyhj",
    "lsrivfztzbdxpkenaxmuwigchj", "lqkivfotzbdxpkenaqmuwygcht", "wsdivfotzbdxpkenbqmuwygchj",
    "lsrlvfotzadxpkencqmuwygchj", "lsrivfotoohxpkenaqmuwygchj", "lsrivfbuzbdfpkenaqmuwygchj",
    "psrivfotzbdxpkenawmuqygchj", "lsrivmotzbdxpkxnaqmuwcychj", "lsrivfotzvdgpkenaqmuwlgchj",
    "lcfivfstzbdxpkenaqmuwygchj", "lsrivfotzbddpkeeaqmuwygcij", "lsribfotzbdxpkenaqmuwugcyj",
    "lsrivfotzbdxakenaqmkwygyhj", "lsrivfotzbdxpkegaqmupyvchj", "lfrivfitzbdxpkenaqmuwygcrj",
    "lskivfotzbdxpkenaqmuwygwwj", "lsrivfotzddnpkenaqmuwfgchj", "lsrivfotzbdiukhnaqmuwygchj",
    "lfrivfotzbdxpkendqmuwygctj", "ljriqfotzvdxpkenaqmuwygchj", "lsrivfotzbdxpkeskqpuwygchj",
    "lsrivfotzbdxpkehaqmupygghj", "lsriyfotsbdxpkedaqmuwygchj", "lsrivfotzbdsjsenaqmuwygchj",
    "lsrivfotzbwxpienaqmuaygchj", "lsrivrotzbdxpkenaumuwygahj", "lsrivpotzfdxpkenaqmuwyjchj",
    "lsrivfomebdxpoenaqmuwygchj", "lswigfotpbdxpkenaqmuwygchj", "lsrivnotzbdxpkenaqmufrgchj",
    "lsrivfolbbdxpkenaqmuwygcqj", "lirivfotzbdxpknnaqeuwygchj", "lsrrvfxtzbdxpaenaqmuwygchj",
    "lspivfotzbdxpnsnaqmuwygchj", "lsrivfotzbyxpkenaqmawygcij", "lsrivfotzbfxpbenaqmuwyichj",
    "lsrivfotzbvxpjeyaqmuwygchj", "lyrihfotzbdxpknnaqmuwygchj", "uurivfotzbdxpkenaqmubygchj",
    "lsrivfotgbdxnkenaxmuwygchj", "lsriffotzbdxpkdnaqmuwygshj", "lsrisfotzbdxpkenaqzjwygchj",
    "lsrilfotzbdxpkenaqmuwygtgj", "lsrivfotzbdxzkenaqmuhmgchj", "hsrivfotzbdxprenaqauwygchj",
    "tsrevfotzbdupkenaqmuwygchj", "lsrizfotzbpxpkenaqmuwyrchj", "lsdivfotzbxxpkenaqmuhygchj",
    "lsrivfttzbyxpkenaqmuaygchj", "lsrivfotzodxpwenaqzuwygchj", "lsrivfotfbdxpkenaqvuwygyhj",
    "lsrivfotzzdxpknnaqmulygchj", "lsrjvvotzbdxpkenaqmuwjgchj", "lsrivuotzbdxpkeiaqxuwygchj",
    "lsrivfotzbdxpzenaqmmwygthj", "lsrivfotzbdxphenaqmuwyghvj"];

pub fn first() -> i32 {
    let mut twos = 0;
    let mut threes = 0;

    for w in INPUT.iter() {

        // Extract a vec<char> and sort it
        let mut word: Vec<char> = w.chars().collect();
        word.sort();

        let mut counts = [0; 26]; // Number of a's counted in [0], bs in [1] etc.

        // For each char in word count the number of times it exists
        for c in &word {
            let ord = (*c as u8 - 'a' as u8) as usize;

            if ord < counts.len() {
                counts[ord] += 1;
            }
        }

        // If a character was counted twice increase twos (but only once each word)
        // Do the same for characters that were counted thrice into threes
        let mut tw = 0;
        let mut th = 0;
        for count in counts.iter() {
            if *count == 2 {
                tw += 1;
            } else if *count == 3 {
                th += 1;
            }
        }

        twos += if tw > 0 { 1 } else { 0 };
        threes += if th > 0 { 1 } else { 0 };
    }

    twos * threes
}

fn identical_chars(a: &Vec<char>, b: &Vec<char>) -> Vec<char>
{
    /*!
        Returns a vector of chars that were at the same position in a and b
    */
    assert_eq!(a.len(), b.len());

    let mut r = vec!();
    for i in 0..a.len() {
        if a[i] == b[i] {
            r.push(a[i]);
        }
    }

    r
}

pub fn second() -> String {
    let mut words = vec!();

    // Put all words in a vec
    for w in INPUT.iter() {
        let ws = w.chars().collect();
        words.push(ws);
    }


    // Check identical chars. If number of identical chars is words.len() - 1 only one is different
    let mut identical: Vec<char> = vec![];
    'finished: for i in 0..words.len() {
        for j in i + 1..words.len() {
            identical = identical_chars(&words[i], &words[j]);

            if identical.len() == words[i].len() - 1 {
                break 'finished;
            }
        }
    }

    use std::iter::FromIterator;

    String::from_iter(identical)
}

